import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button
def check_keydown_events(event,ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True    
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        # 创建一个新的子弹 限制子弹的数量
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False     

def check_events(ai_settings,screen,stats, sb,play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen, ship,aliens, bullets, stats,sb, play_button, mouse_x, mouse_y)

def check_play_button(ai_settings,screen, ship,aliens, bullets, stats,sb, play_button, mouse_x, mouse_y):
    # 在玩家单击 Play 的时候开始游戏
    if play_button.rect.collidepoint(mouse_x, mouse_y) and  not stats.game_active:
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        #  重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        ai_settings.initialize_dynamic_settings()
        stats.game_active = True
        clear_reset(ai_settings, screen, stats,ship, aliens, bullets)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # 屏幕填充，刷新飞船，刷新屏幕
    screen.fill(ai_settings.bg_color)
    # 绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    # for alien in aliens.sprites():
        # alien.blitme()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

# 计算一行可以放多少个外星人
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

# 计算可容纳多少外星人
def get_number_aliens_y(ai_settings, ship_height,  alien_height):
    available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(available_space_y/ (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建外形人群
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width 
    alien.x = alien_width + 2 * alien_width *alien_number
    alien.rect.x = alien.x 
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def creat_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings,screen)

    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_aliens_y(ai_settings,ship.rect.height,alien.rect.height)
    #  创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens,alien_number,row_number)
    
def check_fleet_edges(ai_settings, aliens):
    # 有外星人到达边缘的时候才去相应的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def clear_reset(ai_settings, screen, stats,ship, aliens, bullets):
        # 清空 外星人 和 子弹
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人， 放置飞船
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # 剩余命数减一
    stats.ships_left -= 1
    if stats.ships_left == 0:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    else:
        sb.prep_ships()
        clear_reset(ai_settings, screen, stats,ship, aliens, bullets)
        # 暂停
        sleep(0.5)
def check_aliens_bottom(ai_settings, stats, sb,screen, ship, aliens, bullets):
    # 检查是否有外星人到了底部
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if  alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞一样处理
            ship_hit(ai_settings, stats, sb,screen, ship, aliens, bullets)
            break

def update_aliens(ai_settings,stats,sb,screen, ship, aliens, bullets):
    # 检测是否外星人到达屏幕边缘
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 飞船 与 外星人 碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def update_bullets(bullets, aliens,ai_settings,screen,stats, sb, ship): 
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 代表两个碰撞，然后删除，true 是删除， false 不删除。
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)    
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.inc_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
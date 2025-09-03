import pygame
import sys
import os
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout, QColorDialog, QDialog, QFormLayout, QSpinBox, QLabel, QPlainTextEdit, QMenu, QInputDialog, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QAction

"""Bu Kod SushForAhki tarafından herkese ücretsiz ve açık kaynak olarak yayınlanmıştır bu kodu istediğiniz gibi modefiye edebilirsiniz"""


# GameObject sınıfı, oyun dünyasındaki her nesneyi temsil eder.
class GameObject:
    """Oyun dünyasındaki her nesneyi temsil eder."""
    def __init__(self, x, y, width, height, color, type):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.type = type
        self.images = {}
        self.load_images()

    def load_images(self):
        """Özel çizimler için yüzeyleri (surfaces) oluşturur."""
        if self.type == 'spike':
            surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            self._draw_spike_surface(surface, self.color)
            self.images['default'] = surface
        elif self.type == 'npc':
            surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            self._draw_character(surface, (0, 0, 255), (150, 255, 150), (255, 255, 0))
            self.images['default'] = surface

    def _draw_spike_surface(self, surface, color):
        """Bir diken yüzeyi çizer."""
        points = [
            (0, self.rect.height),
            (self.rect.width / 4, 0),
            (self.rect.width / 2, self.rect.height),
            (self.rect.width * 3 / 4, 0),
            (self.rect.width, self.rect.height)
        ]
        pygame.draw.polygon(surface, color, points)

    def _draw_character(self, surface, body_color, arm_color, head_color):
        """Bir karakter (oyuncu/NPC) çizer."""
        head_rect = pygame.Rect(surface.get_width() * 0.25, 0, surface.get_width() * 0.5, surface.get_height() * 0.2)
        pygame.draw.rect(surface, head_color, head_rect)
        body_rect = pygame.Rect(surface.get_width() * 0.25, surface.get_height() * 0.2, surface.get_width() * 0.5, surface.get_height() * 0.4)
        pygame.draw.rect(surface, body_color, body_rect)
        arm_left = pygame.Rect(0, surface.get_height() * 0.2, surface.get_width() * 0.25, surface.get_height() * 0.4)
        arm_right = pygame.Rect(surface.get_width() * 0.75, surface.get_height() * 0.2, surface.get_width() * 0.25, surface.get_height() * 0.4)
        pygame.draw.rect(surface, arm_color, arm_left)
        pygame.draw.rect(surface, arm_right, arm_right)
        leg_left = pygame.Rect(surface.get_width() * 0.25, surface.get_height() * 0.6, surface.get_width() * 0.2, surface.get_height() * 0.4)
        leg_right = pygame.Rect(surface.get_width() * 0.55, surface.get_height() * 0.6, surface.get_width() * 0.2, surface.get_height() * 0.4)
        pygame.draw.rect(surface, (0, 0, 255), leg_left)
        pygame.draw.rect(surface, (0, 0, 255), leg_right)

    def draw(self, screen):
        """Nesneyi ekrana çizer."""
        draw_color = self.color
        
        if self.type in ['box', 'baseplate']:
            pygame.draw.rect(screen, draw_color, self.rect)
        elif self.type == 'circle':
            pygame.draw.circle(screen, draw_color, self.rect.center, self.rect.width // 2)
        elif self.type == 'triangle':
            p1 = (self.rect.midtop[0], self.rect.midtop[1])
            p2 = (self.rect.bottomleft[0], self.rect.bottomleft[1])
            p3 = (self.rect.bottomright[0], self.rect.bottomright[1])
            pygame.draw.polygon(screen, draw_color, [p1, p2, p3])
        elif self.type == 'star':
            self._draw_star(screen, draw_color)
        elif self.type == 'diamond':
            points = [(self.rect.centerx, self.rect.y), (self.rect.right, self.rect.centery),
                      (self.rect.centerx, self.rect.bottom), (self.rect.left, self.rect.centery)]
            pygame.draw.polygon(screen, draw_color, points)
        elif self.type == 'car':
            self._draw_car(screen, draw_color)
        elif self.type == 'house':
            self._draw_house(screen, draw_color)
        elif self.type == 'building':
            self._draw_building(screen, draw_color)
        elif self.type == 'spawn_point':
            pygame.draw.circle(screen, (0, 255, 0), self.rect.center, 10)
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, 5)
        elif self.type == 'finish_line':
            self._draw_finish_line(screen, draw_color)
        elif self.type == 'spike':
            self._draw_spike(screen)
        elif self.type == 'npc':
            self._draw_npc(screen)
        elif self.type == 'teleport':
            self._draw_teleport(screen, draw_color)

    def _draw_star(self, screen, color):
        """Bir yıldız şekli çizer."""
        center_x, center_y = self.rect.centerx, self.rect.centery
        radius = self.rect.width / 2
        points = []
        for i in range(5):
            angle = pygame.math.Vector2(0, -radius).rotate(-18 + i * 72)
            points.append((center_x + angle.x, center_y + angle.y))
            angle = pygame.math.Vector2(0, -radius / 2.5).rotate(18 + i * 72)
            points.append((center_x + angle.x, center_y + angle.y))
        pygame.draw.polygon(screen, color, points)

    def _draw_car(self, screen, color):
        """Detaylı bir araba çizer."""
        body_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height * 0.4, self.rect.width, self.rect.height * 0.4)
        pygame.draw.rect(screen, color, body_rect)
        
        roof_rect = pygame.Rect(self.rect.x + self.rect.width * 0.2, self.rect.y, self.rect.width * 0.6, self.rect.height * 0.5)
        pygame.draw.rect(screen, (100, 100, 100), roof_rect)
        
        window_width = self.rect.width * 0.2
        window1 = pygame.Rect(roof_rect.x + roof_rect.width * 0.1, roof_rect.y + roof_rect.height * 0.2, window_width, roof_rect.height * 0.6)
        window2 = pygame.Rect(roof_rect.x + roof_rect.width * 0.7 - window_width, roof_rect.y + roof_rect.height * 0.2, window_width, roof_rect.height * 0.6)
        pygame.draw.rect(screen, (173, 216, 230), window1)
        pygame.draw.rect(screen, (173, 216, 230), window2)
        
        wheel_radius = self.rect.width / 8
        wheel1_pos = (self.rect.x + self.rect.width * 0.25, self.rect.bottom)
        wheel2_pos = (self.rect.right - self.rect.width * 0.25, self.rect.bottom)
        
        pygame.draw.circle(screen, (0, 0, 0), wheel1_pos, wheel_radius)
        pygame.draw.circle(screen, (0, 0, 0), wheel2_pos, wheel_radius)
        
        headlight1 = pygame.Rect(self.rect.right - 5, self.rect.y + self.rect.height * 0.5, 5, 5)
        pygame.draw.rect(screen, (255, 255, 0), headlight1)
        taillight1 = pygame.Rect(self.rect.x, self.rect.y + self.rect.height * 0.5, 5, 5)
        pygame.draw.rect(screen, (255, 0, 0), taillight1)

    def _draw_house(self, screen, color):
        """Basit bir ev çizer."""
        body_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height * 0.2, self.rect.width, self.rect.height * 0.8)
        pygame.draw.rect(screen, color, body_rect)
        
        roof_points = [
            (self.rect.x, body_rect.y),
            (self.rect.x + self.rect.width / 2, self.rect.y),
            (self.rect.x + self.rect.width, body_rect.y)
        ]
        pygame.draw.polygon(screen, (139, 69, 19), roof_points)
        
        door_width = self.rect.width * 0.3
        door_height = body_rect.height * 0.6
        door_rect = pygame.Rect(body_rect.centerx - door_width / 2, body_rect.bottom - door_height, door_width, door_height)
        pygame.draw.rect(screen, (100, 50, 0), door_rect)
        
        window_size = min(self.rect.width, self.rect.height) * 0.2
        window_rect = pygame.Rect(body_rect.centerx - window_size / 2, body_rect.y + body_rect.height * 0.2, window_size, window_size)
        pygame.draw.rect(screen, (173, 216, 230), window_rect)
        
    def _draw_building(self, screen, color):
        """Çok katlı bir bina çizer."""
        pygame.draw.rect(screen, color, self.rect)
        
        window_width = self.rect.width * 0.25
        window_height = self.rect.height * 0.15
        
        num_floors = 4
        
        for floor in range(num_floors):
            floor_y = self.rect.bottom - (floor + 1) * (self.rect.height / (num_floors + 1)) - 10
            
            window_rect1 = pygame.Rect(self.rect.x + self.rect.width * 0.15, floor_y, window_width, window_height)
            pygame.draw.rect(screen, (173, 216, 230), window_rect1)
            
            window_rect2 = pygame.Rect(self.rect.right - self.rect.width * 0.15 - window_width, floor_y, window_width, window_height)
            pygame.draw.rect(screen, (173, 216, 230), window_rect2)
            
        door_width = self.rect.width * 0.3
        door_height = self.rect.height * 0.2
        door_rect = pygame.Rect(self.rect.centerx - door_width / 2, self.rect.bottom - door_height, door_width, door_height)
        pygame.draw.rect(screen, (100, 50, 0), door_rect)

    def _draw_finish_line(self, screen, color):
        """Damalı bir bitiş çizgisi çizer."""
        tile_size = 10
        for y in range(self.rect.y, self.rect.bottom, tile_size):
            for x in range(self.rect.x, self.rect.right, tile_size):
                if (x // tile_size + y // tile_size) % 2 == 0:
                    pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, tile_size, tile_size))
                    
    def _draw_spike(self, screen):
        """Özel çizim yüzeyini kullanarak dikeni çizer."""
        if 'default' in self.images:
            screen.blit(self.images['default'], self.rect)
        else:
            self._draw_spike_surface(screen, self.color)
            
    def _draw_npc(self, screen):
        """Özel çizim yüzeyini kullanarak NPC'yi çizer."""
        if 'default' in self.images:
            screen.blit(self.images['default'], self.rect)
        else:
            self._draw_character(screen, (0, 0, 255), (150, 255, 150), (255, 255, 0))

    def _draw_teleport(self, screen, color):
        """Bir ışınlanma noktası çizer."""
        pygame.draw.circle(screen, color, self.rect.center, self.rect.width // 2)
        pygame.draw.line(screen, (255, 255, 255), self.rect.topleft, self.rect.bottomright, 3)
        pygame.draw.line(screen, (255, 255, 255), self.rect.topright, self.rect.bottomleft, 3)

# Player sınıfı, test modundaki oyuncu karakterini temsil eder.
class Player:
    """Test modundaki oyuncu karakteri."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 50)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False
        self.is_driving = False
        
        self.image_idle = self._create_player_image((255, 255, 0), (0, 255, 0), (0, 0, 255), False)
        self.image_walk_right = self._create_player_image((255, 255, 0), (0, 255, 0), (0, 0, 255), True)
        self.image_jump = self._create_player_image((255, 255, 0), (0, 255, 0), (0, 0, 255), False, jump=True)
        self.image = self.image_idle

    def _create_player_image(self, head_color, body_color, leg_color, walking, jump=False):
        """Oyuncu için özel bir yüzey çizer."""
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        head_rect = pygame.Rect(surface.get_width() * 0.25, 0, surface.get_width() * 0.5, surface.get_height() * 0.2)
        pygame.draw.rect(surface, head_color, head_rect)
        body_rect = pygame.Rect(surface.get_width() * 0.25, surface.get_height() * 0.2, surface.get_width() * 0.5, surface.get_height() * 0.4)
        pygame.draw.rect(surface, body_color, body_rect)
        arm_left = pygame.Rect(0, surface.get_height() * 0.2, surface.get_width() * 0.25, surface.get_height() * 0.4)
        arm_right = pygame.Rect(surface.get_width() * 0.75, surface.get_height() * 0.2, surface.get_width() * 0.25, surface.get_height() * 0.4)
        pygame.draw.rect(surface, head_color, arm_left)
        pygame.draw.rect(surface, head_color, arm_right)
        leg_left = pygame.Rect(surface.get_width() * 0.25, surface.get_height() * 0.6, surface.get_width() * 0.2, surface.get_height() * 0.4)
        leg_right = pygame.Rect(surface.get_width() * 0.55, surface.get_height() * 0.6, surface.get_width() * 0.2, surface.get_height() * 0.4)
        pygame.draw.rect(surface, leg_color, leg_left)
        pygame.draw.rect(surface, leg_color, leg_right)

        if jump:
            rotated_arm_left = pygame.transform.rotate(surface, 45)
            rotated_arm_right = pygame.transform.rotate(surface, -45)
            surface.blit(rotated_arm_left, arm_left)
            surface.blit(rotated_arm_right, arm_right)
            
        return surface

    def update(self, obstacles):
        """Oyuncu konumunu günceller ve çarpışmaları yönetir."""
        if not self.is_driving:
            self.vel_y += self.gravity

        self.rect.x += self.vel_x
        self.on_ground = False
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.vel_x > 0:
                    self.rect.right = obstacle.rect.left
                elif self.vel_x < 0:
                    self.rect.left = obstacle.rect.right
        
        self.rect.y += self.vel_y
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.vel_y > 0:
                    self.rect.bottom = obstacle.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = obstacle.rect.bottom
                    self.vel_y = 0
    
    def handle_image(self):
        """Oyuncu durumuna göre gösterilecek görüntüyü ayarlar."""
        if not self.on_ground:
            self.image = self.image_jump
        elif self.vel_x > 0:
            self.image = self.image_walk_right
        elif self.vel_x < 0:
            self.image = pygame.transform.flip(self.image_walk_right, True, False)
        else:
            self.image = self.image_idle

    def jump(self):
        """Oyuncunun zıplamasını sağlar."""
        if self.on_ground and not self.is_driving:
            self.vel_y = self.jump_power

    def draw(self, screen):
        """Güncel görüntüyü ekrana çizer."""
        self.handle_image()
        screen.blit(self.image, self.rect)

# NPC sınıfı, otomatik hareket eden karakterler için.
class NPC(GameObject):
    """Engellere çarptığında yön değiştiren otomatik hareketli NPC."""
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color, 'npc')
        self.speed = 2
        self.direction = 1
        self.image = self.images.get('default', pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA))
    
    def update(self, obstacles):
        """NPC'nin konumunu günceller ve çarpışmaları yönetir."""
        self.rect.x += self.speed * self.direction
        
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect) and obstacle.type not in ['npc', 'player']:
                self.direction *= -1
                self.rect.x += self.speed * self.direction

        if self.direction < 0:
            self.image = pygame.transform.flip(self.images.get('default'), True, False)
        else:
            self.image = self.images.get('default')

    def draw(self, screen):
        """NPC'yi ekrana çizer."""
        screen.blit(self.image, self.rect)

# Nesne özelliklerini düzenlemek için iletişim kutusu.
class PropertiesDialog(QDialog):
    def __init__(self, parent, game_object):
        super().__init__(parent)
        self.setWindowTitle("Nesne Özellikleri")
        self.game_object = game_object
        self.new_color = game_object.color
        
        self.layout = QFormLayout(self)

        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(10, 500)
        self.width_spinbox.setValue(game_object.rect.width)
        self.layout.addRow(QLabel("Genişlik:"), self.width_spinbox)
        
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(10, 500)
        self.height_spinbox.setValue(game_object.rect.height)
        self.layout.addRow(QLabel("Yükseklik:"), self.height_spinbox)
        
        self.color_button = QPushButton("Renk Seç")
        self.color_button.clicked.connect(self.select_color)
        self.layout.addRow(QLabel("Renk:"), self.color_button)

        self.ok_button = QPushButton("Uygula")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

    def select_color(self):
        """Renk seçme iletişim kutusunu açar."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.new_color = color.getRgb()[:3]
            self.game_object.color = self.new_color
            
    def get_properties(self):
        """Değiştirilen özellikleri döndürür."""
        return {
            "width": self.width_spinbox.value(),
            "height": self.height_spinbox.value(),
            "color": self.new_color
        }

# Ana uygulama penceresi ve UI yönetimi.
class BricksyBuilder(QMainWindow):
    """Ana uygulama penceresini ve UI elemanlarını yönetir."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brickscy Builder")
        self.setGeometry(100, 100, 1200, 800)
        self.is_test_mode = False

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)

        self.objects = [GameObject(0, 700, 2000, 100, (150, 150, 150), 'baseplate')]
        
        self.background_color = (255, 255, 255)
        
        self.left_panel = QVBoxLayout()
        self.main_layout.addLayout(self.left_panel)

        self.box_button = QPushButton("Kutu Ekle")
        self.box_button.clicked.connect(lambda: self.pygame_widget.set_tool('box'))
        self.left_panel.addWidget(self.box_button)

        self.circle_button = QPushButton("Daire Ekle")
        self.circle_button.clicked.connect(lambda: self.pygame_widget.set_tool('circle'))
        self.left_panel.addWidget(self.circle_button)
        
        self.triangle_button = QPushButton("Üçgen Ekle")
        self.triangle_button.clicked.connect(lambda: self.pygame_widget.set_tool('triangle'))
        self.left_panel.addWidget(self.triangle_button)

        self.star_button = QPushButton("Yıldız Ekle")
        self.star_button.clicked.connect(lambda: self.pygame_widget.set_tool('star'))
        self.left_panel.addWidget(self.star_button)
        
        self.diamond_button = QPushButton("Elmas Ekle")
        self.diamond_button.clicked.connect(lambda: self.pygame_widget.set_tool('diamond'))
        self.left_panel.addWidget(self.diamond_button)
        
        self.car_button = QPushButton("Araç Ekle")
        self.car_button.clicked.connect(lambda: self.pygame_widget.set_tool('car'))
        self.left_panel.addWidget(self.car_button)

        self.house_button = QPushButton("Ev Ekle")
        self.house_button.clicked.connect(lambda: self.pygame_widget.set_tool('house'))
        self.left_panel.addWidget(self.house_button)

        self.building_button = QPushButton("Bina Ekle")
        self.building_button.clicked.connect(lambda: self.pygame_widget.set_tool('building'))
        self.left_panel.addWidget(self.building_button)

        self.spawn_button = QPushButton("Başlangıç Noktası Ekle")
        self.spawn_button.clicked.connect(lambda: self.pygame_widget.set_tool('spawn_point'))
        self.left_panel.addWidget(self.spawn_button)

        self.finish_line_button = QPushButton("Bitiş Çizgisi Ekle")
        self.finish_line_button.clicked.connect(lambda: self.pygame_widget.set_tool('finish_line'))
        self.left_panel.addWidget(self.finish_line_button)
        
        self.spike_button = QPushButton("Diken Ekle")
        self.spike_button.clicked.connect(lambda: self.pygame_widget.set_tool('spike'))
        self.left_panel.addWidget(self.spike_button)

        self.npc_button = QPushButton("NPC Ekle")
        self.npc_button.clicked.connect(lambda: self.pygame_widget.set_tool('npc'))
        self.left_panel.addWidget(self.npc_button)

        self.teleport_button = QPushButton("Işınlanma Noktası Ekle")
        self.teleport_button.clicked.connect(lambda: self.pygame_widget.set_tool('teleport'))
        self.left_panel.addWidget(self.teleport_button)

        self.background_button = QPushButton("Arka Plan Rengi")
        self.background_button.clicked.connect(self.change_background)
        self.left_panel.addWidget(self.background_button)
        
        self.left_panel.addWidget(QLabel("--- Nesne Gezgini ---"))
        self.object_list_widget = QListWidget()
        self.left_panel.addWidget(self.object_list_widget)
        self.object_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.object_list_widget.customContextMenuRequested.connect(self.show_explorer_context_menu)
        
        self.left_panel.addStretch()
        
        # Pygame widget (sağ panel).
        self.right_panel = QVBoxLayout()
        self.main_layout.addLayout(self.right_panel, 1)

        self.pygame_widget = PygameWidget(self.objects, self)
        self.right_panel.addWidget(self.pygame_widget, 1)
        
        self.pygame_widget.setFocus()
        
        # Konsol paneli (sağ alt).
        self.console_panel = QPlainTextEdit()
        self.console_panel.setReadOnly(True)
        self.console_panel.setMaximumHeight(150)
        self.right_panel.addWidget(self.console_panel)
        self.log_message("Brickscy Builder'a hoş geldiniz! F5'e basarak oyunu test edebilir, F11 ile tam ekrana geçebilir, Ctrl+C ve Ctrl+V ile objeleri kopyalayıp yapıştırabilirsiniz.")
        self.update_explorer_list()

    def show_explorer_context_menu(self, pos):
        """Gezginde bir öğeye sağ tıklandığında menüyü gösterir."""
        item = self.object_list_widget.itemAt(pos)
        if item:
            menu = QMenu(self)
            delete_action = menu.addAction("Sil")
            action = menu.exec(self.object_list_widget.mapToGlobal(pos))
            if action == delete_action:
                index = self.object_list_widget.row(item)
                self.delete_object_from_explorer(index)
    
    def delete_object_from_explorer(self, index):
        """Listeden ve oyundan bir nesneyi siler."""
        if 0 <= index < len(self.objects):
            if self.objects[index].type == 'baseplate':
                self.log_message("Zemin plakası silinemez.")
                return
            self.objects.pop(index)
            self.object_list_widget.takeItem(index)
            self.log_message(f"Nesne silindi.")

    def log_message(self, message):
        """Konsol paneline bir mesaj ekler."""
        self.console_panel.appendPlainText(message)

    def update_explorer_list(self):
        """Gezgin panelindeki nesne listesini günceller."""
        self.object_list_widget.clear()
        for i, obj in enumerate(self.objects):
            item_text = f"({i}) - {obj.type.capitalize()}"
            self.object_list_widget.addItem(item_text)

    def change_background(self):
        """Arka plan rengini değiştirmek için bir renk iletişim kutusu açar."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.background_color = color.getRgb()[:3]
            self.pygame_widget.background_color = self.background_color

# PygameWidget sınıfı, editörün görsel arayüzünün kalbidir.
class PygameWidget(QWidget):
    """PyQt arayüzü içinde Pygame çizimlerini gösteren özel bir widget."""
    def __init__(self, objects, parent):
        super().__init__()
        self.objects = objects
        self.parent = parent
        self.current_tool = 'box'
        self.selected_object = None
        self.drag_offset = (0, 0)
        self.background_color = (255, 255, 255)
        self.clipboard_object = None
        
        self.is_test_mode = False
        self.player = None
        self.car = None
        
        os.environ['SDL_WINDOWID'] = str(self.winId().__int__())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pygame_screen)
        self.timer.start(1000 // 60)
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
    def set_tool(self, tool_name):
        """Yeni nesne oluşturmak için aktif aracı ayarlar."""
        if self.is_test_mode:
            self.parent.log_message("Test modundayken araç değiştirilemez.")
            return
        self.current_tool = tool_name
        self.parent.log_message(f"Aktif araç: {tool_name}")

    def mousePressEvent(self, event):
        """Nesne oluşturma ve sürükleme için fare basma olaylarını yönetir."""
        if self.is_test_mode:
            return

        x, y = event.pos().x(), event.pos().y()
        
        if event.button() == Qt.MouseButton.RightButton:
            clicked_obj = None
            for obj in self.objects:
                if obj.rect.collidepoint(x, y):
                    clicked_obj = obj
                    break
            
            if clicked_obj:
                self.show_context_menu(clicked_obj, event.pos())
                return
        
        if event.button() == Qt.MouseButton.LeftButton:
            for obj in reversed(self.objects):
                if obj.rect.collidepoint(x, y) and obj.type != 'baseplate':
                    self.selected_object = obj
                    self.drag_offset = (x - obj.rect.x, y - obj.rect.y)
                    return
            
            color_map = {
                'box': (255, 0, 0),
                'circle': (0, 0, 255),
                'triangle': (0, 255, 0),
                'star': (255, 255, 0),
                'diamond': (0, 255, 255),
                'car': (100, 100, 100),
                'house': (139, 69, 19),
                'building': (192, 192, 192),
                'spawn_point': (0, 0, 0),
                'finish_line': (0, 0, 0),
                'spike': (255, 0, 0),
                'npc': (255, 255, 0),
                'teleport': (138, 43, 226)
            }
            color = color_map.get(self.current_tool, (255, 255, 255))
            
            if self.current_tool == 'npc':
                new_object = NPC(x, y, 50, 50, color)
            else:
                new_object = GameObject(x, y, 50, 50, color, self.current_tool)
            self.objects.append(new_object)
            self.parent.update_explorer_list()

    def show_context_menu(self, obj, pos):
        """Seçili nesne için bir bağlam menüsü gösterir."""
        menu = QMenu(self)
        
        edit_action = menu.addAction("Özellikleri Düzenle")
        edit_action.triggered.connect(lambda: self.open_properties_dialog(obj))
        
        delete_action = menu.addAction("Sil")
        delete_action.triggered.connect(lambda: self.delete_object(obj))
        
        menu.exec(self.mapToGlobal(pos))

    def delete_object(self, obj):
        """Bir oyun nesnesini siler."""
        if obj.type == 'baseplate':
            self.parent.log_message("Zemin plakası silinemez.")
            return

        self.objects.remove(obj)
        self.parent.update_explorer_list()
        self.parent.log_message(f"Nesne silindi.")

    def mouseMoveEvent(self, event):
        """Nesneleri sürüklemek için fare hareket olaylarını yönetir."""
        if self.is_test_mode:
            return
            
        if self.selected_object and event.buttons() == Qt.MouseButton.LeftButton:
            x, y = event.pos().x(), event.pos().y()
            self.selected_object.rect.x = x - self.drag_offset[0]
            self.selected_object.rect.y = y - self.drag_offset[1]
            self.parent.update_explorer_list()

    def mouseReleaseEvent(self, event):
        """Fare bırakıldığında seçili nesneyi sıfırlar."""
        if self.is_test_mode:
            return
            
        if event.button() == Qt.MouseButton.LeftButton:
            self.selected_object = None

    def keyPressEvent(self, event):
        """Klavye tuş basma olaylarını yönetir."""
        if event.key() == Qt.Key.Key_F5:
            self.is_test_mode = not self.is_test_mode
            self.parent.log_message(f"Test modu: {'Açık' if self.is_test_mode else 'Kapalı'}")
            if self.is_test_mode:
                spawn_point_found = False
                for obj in self.objects:
                    if obj.type == 'spawn_point':
                        self.player = Player(obj.rect.x, obj.rect.y)
                        spawn_point_found = True
                        break
                if not spawn_point_found:
                    self.player = Player(100, 100)
                
            else:
                self.player = None
                self.car = None
        
        if event.key() == Qt.Key.Key_F11:
            if self.parent.isFullScreen():
                self.parent.showNormal()
            else:
                self.parent.showFullScreen()
        
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_C:
            if self.selected_object and self.selected_object.type != 'baseplate':
                self.clipboard_object = self.selected_object
                self.parent.log_message("Nesne kopyalandı.")
            else:
                self.parent.log_message("Lütfen kopyalamak için bir nesne seçin.")
        
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_V:
            if self.clipboard_object:
                new_object_type = self.clipboard_object.type
                new_object_color = self.clipboard_object.color
                
                if new_object_type == 'npc':
                    new_object = NPC(
                        self.clipboard_object.rect.x + 20, 
                        self.clipboard_object.rect.y + 20, 
                        self.clipboard_object.rect.width, 
                        self.clipboard_object.rect.height, 
                        new_object_color
                    )
                else:
                    new_object = GameObject(
                        self.clipboard_object.rect.x + 20, 
                        self.clipboard_object.rect.y + 20, 
                        self.clipboard_object.rect.width, 
                        self.clipboard_object.rect.height, 
                        new_object_color, 
                        new_object_type
                    )
                self.objects.append(new_object)
                self.parent.update_explorer_list()
                self.parent.log_message("Nesne yapıştırıldı.")
            else:
                self.parent.log_message("Yapıştırılacak bir nesne yok.")

        if self.is_test_mode and self.player:
            if event.key() in [Qt.Key.Key_D, Qt.Key.Key_Right]:
                self.player.vel_x = self.player.speed
            elif event.key() in [Qt.Key.Key_A, Qt.Key.Key_Left]:
                self.player.vel_x = -self.player.speed
            elif event.key() == Qt.Key.Key_Space:
                self.player.jump()
                
    def keyReleaseEvent(self, event):
        """Tuş bırakma olaylarını yöneterek oyuncu hareketini durdurur."""
        if self.is_test_mode and self.player:
            if event.key() in [Qt.Key.Key_D, Qt.Key.Key_A, Qt.Key.Key_Right, Qt.Key.Key_Left]:
                self.player.vel_x = 0

    def open_properties_dialog(self, game_object):
        """Nesne özelliklerini düzenlemek için iletişim kutusunu açar."""
        dialog = PropertiesDialog(self, game_object)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            props = dialog.get_properties()
            game_object.rect.width = props['width']
            game_object.rect.height = props['height']
            game_object.color = props['color']
            game_object.load_images()
    
    def update_pygame_screen(self):
        """Pygame render ve olay işleme için ana döngü."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.parent.close()
        
        self.screen.fill(self.background_color)
        
        if not self.is_test_mode:
            for obj in self.objects:
                obj.draw(self.screen)
        else:
            non_player_objects = [obj for obj in self.objects if obj.type not in ['player', 'npc']]
            
            for obj in self.objects:
                if isinstance(obj, NPC):
                    obj.update(non_player_objects)

            if self.player:
                if not self.player.is_driving:
                    for obj in non_player_objects:
                        if obj.type == 'car' and self.player.rect.colliderect(obj.rect.inflate(10, 10)):
                            self.player.is_driving = True
                            self.car = obj
                            break
                
                if self.player.is_driving and self.car:
                    self.player.rect.x = self.car.rect.x
                    self.player.rect.y = self.car.rect.y
                    self.car.rect.x += self.player.vel_x
                    
                self.player.update(non_player_objects)
            
            for obj in self.objects:
                obj.draw(self.screen)

            if self.player:
                for obj in self.objects:
                    if obj.type == 'finish_line' and self.player.rect.colliderect(obj.rect):
                        self.parent.log_message("KAZANDINIZ!")
                        self.is_test_mode = False
                        self.player = None
                        self.car = None
                        break
                    elif obj.type == 'spike' and self.player.rect.colliderect(obj.rect):
                        self.parent.log_message("Dikenlere çarptın! Başa dönüyorsun...")
                        spawn_point = next((o for o in self.objects if o.type == 'spawn_point'), None)
                        if spawn_point:
                            self.player.rect.topleft = spawn_point.rect.topleft
                            self.player.vel_x = 0
                            self.player.vel_y = 0
                        else:
                            self.player.rect.topleft = (100, 100)
                            self.player.vel_x = 0
                            self.player.vel_y = 0
                        break
                    elif obj.type == 'teleport' and self.player.rect.colliderect(obj.rect):
                        teleport_points = [o for o in self.objects if o.type == 'teleport' and o != obj]
                        if teleport_points:
                            destination = teleport_points[0]
                            self.player.rect.topleft = destination.rect.topleft
                            self.parent.log_message("Işınlandın!")
                        else:
                            spawn_point = next((o for o in self.objects if o.type == 'spawn_point'), None)
                            if spawn_point:
                                self.player.rect.topleft = spawn_point.rect.topleft
                            else:
                                self.player.rect.topleft = (100, 100)
                            self.parent.log_message("Işınlanma noktası yok, başlangıç noktasına döndün.")
                            
                self.player.draw(self.screen)
        
        pygame.display.flip()

# Uygulamanın giriş noktası.
if __name__ == '__main__':
    pygame.init()
    app = QApplication(sys.argv)
    window = BricksyBuilder()
    window.show()
    sys.exit(app.exec())
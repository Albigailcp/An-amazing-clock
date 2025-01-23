import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_ESCAPE, QUIT
import random

pygame.init()

# Screen setup
width_screen, height_screen = 500, 500
screen = pygame.display.set_mode((width_screen, height_screen))
bg_day = pygame.image.load('CLOCK.png')  #background image
bg_night = pygame.image.load('CLOCKNIGHT.png')
bg_mid = pygame.image.load('CLOCKMID.png')
minuteshandle_image = pygame.image.load('MINUTES.png')  # Minute hand
hourshandle_image = pygame.image.load('HOURS.png')  # Hour hand

#for dhims reference
fishA=pygame.image.load('FISH1.png')
fishB=pygame.image.load('FISH2.png')
fishC=pygame.image.load('FISH3.png')
fishD=pygame.image.load('FISH4.png')

#for bread everywhere
breadA=pygame.image.load('BREAD1.png')
breadB=pygame.image.load('BREAD2.png')
breadC=pygame.image.load('BREAD3.png')
breadD=pygame.image.load('BREAD4.png')

#for omori reference
omorA=pygame.image.load('OMOR1.png')
omorB=pygame.image.load('OMOR2.png')
omorC=pygame.image.load('OMOR3.png')
omorD=pygame.image.load('OMOR4.png')

#for good omens reference
bookA=pygame.image.load('BOOK1.png')
bookB=pygame.image.load('BOOK2.png')
bookC=pygame.image.load('BOOK3.png')
bookD=pygame.image.load('BOOK4.png')

#for tma reference
tapeA=pygame.image.load('TAPE1.png')
tapeB=pygame.image.load('TAPE2.png')
tapeC=pygame.image.load('TAPE3.png')
tapeD=pygame.image.load('TAPE4.png')

#for confety for finishing a day
confetyA=pygame.image.load('SPRINKLES1.png')
confetyB=pygame.image.load('SPRINKLES2.png')
confetyC=pygame.image.load('SPRINKLES3.png')
confetyD=pygame.image.load('SPRINKLES4.png')

#for lunch
lunchA=pygame.image.load('LUNCH1.png')
lunchB=pygame.image.load('LUNCH2.png')
lunchC=pygame.image.load('LUNCH3.png')
lunchD=pygame.image.load('LUNCH4.png')

#for a snack
snackA=pygame.image.load('SNACK1.png')
snackB=pygame.image.load('SNACK2.png')
snackC=pygame.image.load('SNACK3.png')
snackD=pygame.image.load('SNACK4.png')

#sun and moon and spider
sun_image=pygame.image.load('SUN.png')
moon_image=pygame.image.load('MOON.png')
spider_image=pygame.image.load('SPIDER.png')

# Clock class
class Clock:
    def __init__(self):
      self.hours = 23
      self.minutes = 59
      self.bg = bg_day  # daymode is the default
      self.last_update = 0  #<- for the long key presses
      self.cool_object_list_real = []

    def draw_hand(self, hand_image, pivot, angle):
      """Draw a rotated hand"""
      # Rotate the hand
      rotated_hand = pygame.transform.rotate(hand_image, angle)

      # Adjust for pivot (should align side of the hand to the clock center)
      hand_rect = rotated_hand.get_rect()
      hand_rect.center = pivot  # Start with the clock center as the pivot

      # Draw the rotated hand
      screen.blit(rotated_hand, hand_rect.topleft)
        
    def draw_clock_hands(self):
      """Drawing clock hands"""
      center_of_clock = (width_screen // 2, height_screen // 2)

      # Hands angles!!
      minute_angle = -self.minutes * 6  # 360° / 60 minutes
      hour_angle = -self.hours * 30 - self.minutes * 0.5  # 360° / 12 hours + minute adjustment

      # Draw minute hand
      self.draw_hand(minuteshandle_image, center_of_clock, minute_angle) #with -50 and -25 for the hour it aligns it to the center BUT it doesn't rotate on the base.

      # Draw hour hand
      self.draw_hand(hourshandle_image, center_of_clock, hour_angle)

    def handle_input(self, event):
      """for when the user presses the keys once"""
      if event.type == pygame.KEYDOWN:
          if event.key == K_RIGHT:
              self.increment_time()
          elif event.key == K_LEFT:
              self.decrement_time()

    def increment_time(self):
      """increment the time"""
      self.minutes += 1
      if self.minutes == 60:
          self.minutes = 0
          self.hours = (self.hours + 1) % 24

    def decrement_time(self):
      """decrement the time"""
      self.minutes -= 1
      if self.minutes < 0:
          self.minutes = 59
          self.hours = (self.hours - 1) % 24
          
    def handle_long_press(self):
      """for long key presses, because single ones are slow"""
      keys = pygame.key.get_pressed()
      current_time = pygame.time.get_ticks()
      time_delay=5
      
      if keys[K_RIGHT] and current_time - self.last_update > time_delay:
          self.increment_time()
          self.last_update = current_time
      elif keys[K_LEFT] and current_time - self.last_update > time_delay: 
          self.decrement_time()
          self.last_update = current_time
            
    def modes(self):
      """change from day to nightmode and midday"""
      self.bg=bg_day
      if self.hours>=18 or self.hours<6:
        self.bg=bg_night
      elif self.hours>=13 and self.hours<18:
        self.bg=bg_mid
      else:
        self.bg=bg_day
      
    def drawbackground(self):
      """changing the background"""
      screen.fill((255, 255, 255))  # screen clear
      self.modes() #clock
      screen.blit(self.bg, (0, 0))
      
    def making_cool_things_happen(self,hour,minute,coolobjectarray,elementA,elementB,elementC,elementD):
      if self.hours == hour and self.minutes == minute and len(self.cool_object_list_real) == 0:
            coolobjectarray = [elementA,elementB,elementC,elementD]
            for _ in range(15):  # spawning cool stuff
                coolobject = {
                    "image": random.choice(coolobjectarray),
                    "x": random.randint(0, width_screen - 100),  # random x position
                    "y": random.randint(0,height_screen - 100)  #random y position
                }
                self.cool_object_list_real.append(coolobject)
      for coolobject in self.cool_object_list_real:
            coolobject["y"] += 1  #how fast the fall is
            screen.blit(coolobject["image"], (coolobject["x"], coolobject["y"]))

        #remove objects
      self.cool_object_list_real = [coolobject for coolobject in self.cool_object_list_real if coolobject["y"] < height_screen]
    
    def fishEveryWhere(self):
      fish_list=[]
      self.making_cool_things_happen(9,30,fish_list,fishA,fishB,fishC,fishD)
     
    def breadEveryWhereMorning(self):
      bread_list=[]
      self.making_cool_things_happen(7,30,bread_list,breadA,breadB,breadC,breadD) #Add breads please.
    
    def breadEveryWhereNight(self):
      bread_list2=[]
      self.making_cool_things_happen(20,30,bread_list2,breadA,breadB,breadC,breadD)
    
    def omor(self):
      omor_list=[]
      self.making_cool_things_happen(21,30,omor_list,omorA,omorB,omorC,omorD) #Add windmills please.
    
    def books(self):
      book_list=[]
      self.making_cool_things_happen(18,9,book_list,bookA,bookB,bookC,bookD) #add everything...
    
    def tapes(self):
      tapes_list=[]
      self.making_cool_things_happen(16,0,tapes_list,tapeA,tapeB,tapeC,tapeD)
    
    def one_full_day(self):
      confety_list=[]
      self.making_cool_things_happen(23,59,confety_list,confetyA,confetyB,confetyC,confetyD)
    
    def lunch(self):
      lunch_list=[]
      self.making_cool_things_happen(13,30,lunch_list,lunchA,lunchB,lunchC,lunchD)
    
    def snacktime(self):
      snack_list=[]
      self.making_cool_things_happen(10,0,snack_list,snackA,snackB,snackC,snackD)
    
    def secondsnack(self):
      snack_list2=[]
      self.making_cool_things_happen(17,0,snack_list2,snackA,snackB,snackC,snackD)
      
    def sun_and_moon_and_spider(self,hour,minute,coolobjectarray,element):
      if self.hours == hour and self.minutes == minute and len(self.cool_object_list_real) == 0:
            coolobjectarray = [element]
            for _ in range(1):  # spawning cool stuff
                coolobject = {
                    "image": coolobjectarray[0],
                    "x": (0),  # random x position
                    "y": (0)  #random y position
                }
                self.cool_object_list_real.append(coolobject)

      for coolobject in self.cool_object_list_real:
            coolobject["y"] += 1  
            screen.blit(coolobject["image"], (coolobject["x"], coolobject["y"]))

        #remove objects
      self.cool_object_list_real = [coolobject for coolobject in self.cool_object_list_real if coolobject["y"] < height_screen]      

    def sun(self):
      """for daytime"""
      sun=[]
      self.sun_and_moon_and_spider(6,0,sun,sun_image)

    def moon(self):
      """for nighttime"""
      moon=[]
      self.sun_and_moon_and_spider(19,0,moon,moon_image)

    def spider(self):
      """for 3am a cute spider"""
      spider=[]
      self.sun_and_moon_and_spider(3,0,spider,spider_image)


working_clock = Clock()

# main loop
running = True
while running:
  working_clock.drawbackground()

  for event in pygame.event.get():
      if event.type == QUIT:
          running = False
      elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
          running = False
      working_clock.handle_input(event)

  working_clock.handle_long_press()

  # Update and draw everything
  working_clock.fishEveryWhere()
  working_clock.breadEveryWhereMorning()
  working_clock.breadEveryWhereNight()
  working_clock.omor()
  working_clock.tapes()
  working_clock.one_full_day()
  working_clock.lunch()
  working_clock.snacktime()
  working_clock.secondsnack()
  
  working_clock.sun()
  working_clock.moon()
  working_clock.spider()
  
  working_clock.draw_clock_hands()

  pygame.display.flip()
  pygame.time.Clock().tick(60)  # limit to 60 FPS

pygame.quit()
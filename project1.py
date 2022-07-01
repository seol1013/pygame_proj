#5.게임종료하는 처리
# (1) 모든 공을 없애면 게임 종료
# (2) 캐릭터는 공에 닿으면 게임 종료
# (3) 시간 제한 99초 초과 시 게임 종료
import pygame
import os


pygame.init() 


screen_width = 480
screen_height =  640
screen = pygame.display.set_mode((screen_width, screen_height))


pygame.display.set_caption("pangpang") 


clock = pygame.time.Clock()



current_path = os.path.dirname(__file__) #현제 파일의 위치를 반환
image_path = os.path.join(current_path, "image1") # image1 폴더 위치 반환

#배경만들기
background = pygame.image.load(os.path.join(image_path,"background.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #스테이지의 높이 위에 캐릭터를 두거나 공의 위치를 정하기 위해

#캐릭터 만들기
character = pygame.image.load(os.path.join(image_path,"character1.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height-(stage_height + character_height)

character_to_x = 0



character_speed = 0.5

#무기 만들기
weapon = pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0] #높이는 필요X
#무기 한번에 여러발 발사 가능
weapons = []
#무기 이동속도
weapon_speed = 2

# 공 만들기 (4개 크기에 대해서 따로 처리
ball_images = [
    pygame.image.load(os.path.join(image_path,"balloon1.png")),
    pygame.image.load(os.path.join(image_path,"balloon2.png")),
    pygame.image.load(os.path.join(image_path,"balloon3.png")),
    pygame.image.load(os.path.join(image_path,"balloon4.png"))
]
#공이 클수록 처음 스피드가 큰(공 크기에 따른 최초 스피드)
ball_speed_y = [-18,-15,-12,-9] #바닥에 팅기고 올라갈때는 -가 붙어서 위로 갈거기 때문에 


# 공들
balls = []
balls.append({
    "pos_x":50,
    "pos_y":50,  #공의 x,y좌표
    "img_idx" : 0, #공의 이미지 인덱스
    "to_x" : 3, #공의x축 이동방향 -3이면 왼쪽으로 3이면 오른쪽으로
    "to_y": -6,#공의y축 이동방향
    "init_spd_y": ball_speed_y[0]#y 최초 속도 공마다 스테이지에 팅겼을 때 위로 올라가는게 다르므로 , 
})

#4. 사리질 무기, 공 정보 저장 변수
weapon_to_remove  = -1
ball_to_remove  = -1

# Font 정의
game_font = pygame.font.Font(None,40)
total_time = 9
start_ticks = pygame.time.get_ticks() #시작시간 정의
#게임 종료 메세지 / timeOut(시간 초과), Mission Complete(성공), Game Over(캐릭터 공에 맞음)
game_result = "Game Over"

# 이벤트 루프
running = True 
while running:
    dt = clock.tick(90) 
    #print("fps :"+str(clock.get_fps()))    
    #2. 이벤트 처리 기능(키보드 ,마우스등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            character_to_x -= character_speed 
        elif event.key == pygame.K_RIGHT:
            character_to_x += character_speed
        elif event.key == pygame.K_UP:
            weapon_x_pos = character_x_pos+(character_width/2) - weapon_width/2
            weapon_y_pos = character_y_pos
            weapons.append([weapon_x_pos,weapon_y_pos])


    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            character_to_x =0
        
    
    character_x_pos += character_to_x

    if character_x_pos<0:
        character_x_pos =0
    elif character_x_pos > screen_width-character_width:
         character_x_pos=screen_width-character_width

    #무기 위치 조정 ??? #한줄 for문 다시 공부
    # 100, 200 --> 180 -->160 속도만큼 빼줘서 위로 올림
    weapons =[ [w[0],w[1] - weapon_speed] for w in weapons] #무기 위치를 위로
    #천장에 닿은 무기 없애기
    weapons = [ [ w[0], w[1] ] for w in weapons if w[1] >0]

    # 공 위치 정의
    for ball_idx,ball_val in enumerate(balls): #enumerate:ball 리스트에 있는 것을 하나씩 가져와서 몇 번째 인덱스인지 값을 출력해주는 것
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_image_idx = ball_val["img_idx"]
        
        ball_size = ball_images[ball_image_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        #가로벽에 닿았을 때 공 이동 위치 변경
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] *-1 #벽에 팅겼을 때 반대로 팅기게 하기 위해
        # 세로 위치
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"] # 스테이지에 팅겨서 올라가는 처음
        else: #그 외경우는 그냥 속도를 줄여줌
            ball_val["to_y"] += 0.3
        
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
        
    #4. 충돌처리(만나는 부분이 실행X...!!!!!!!---> 해결)





    #캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    for ball_idx,ball_val in enumerate(balls): 
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        #공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        #공과 캐릭터 충돌처리
        if character_rect.colliderect(ball_rect):
            running = False
            break

        #공과 무기들 충돌처리
        for weapon_idx,weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]
            #무기 rect정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx #해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx #해당 무기 없애기 위한 값 설정
                
                #가장 작은 공이 아니라면 다음 단계의 공인 둘로 나눈어짐
                if ball_image_idx < 3:
                    #현제 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_image_idx +1].get_rect() #실제론 한단계 작은 크기 공이므로
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]
                    
                    

                    #왼쪽으로 튕겨나가는 작은 공 
                    balls.append({
                    "pos_x":ball_pos_x+(ball_width/2) - (small_ball_width/2),
                    "pos_y":ball_pos_y+(ball_height/2) - (small_ball_height/2),  #공의 x,y좌표
                    "img_idx" : ball_image_idx +1, #공의 이미지 인덱스
                    "to_x" : -3, #공의x축 이동방향 -3이면 왼쪽으로 3이면 오른쪽으로
                    "to_y": -6,#공의y축 이동방향
                    "init_spd_y": ball_speed_y[ball_image_idx +1]#y 최초 속도 공마다 스테이지에 팅겼을 때 위로 올라가는게 다르므로 , 
                })  
                #오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x":ball_pos_x+(ball_width/2) - (small_ball_width/2),
                        "pos_y":ball_pos_y+(ball_height/2) - (small_ball_height/2),  #공의 x,y좌표
                        "img_idx" : ball_image_idx +1, #공의 이미지 인덱스
                        "to_x" : 3, #공의x축 이동방향 -3이면 왼쪽으로 3이면 오른쪽으로
                        "to_y": -6,#공의y축 이동방향
                        "init_spd_y": ball_speed_y[ball_image_idx +1]#y 최초 속도 공마다 스테이지에 팅겼을 때 위로 올라가는게 다르므로 , 
                })          
                break
        else:
            continue
        break



    #충돌된 공 or무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1 #다음 프레임에서 이 루트를 타기 위함
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1 #다음 프레임에서 이 루트를 타기 위함
        
    
    #모든 공을 없앤 경우
    if len(balls) ==0:
        game_result = "Mission Complete"
        running = False


    screen.blit(background,(0,0))
    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))
    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))
    #무기는 여러개가 가능하도록 하기 위함

    for idx,val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x,ball_pos_y))
        

    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)),True,(255,0,0))
    screen.blit(timer, (10,10))

    #시간 초과했다면 
    if (total_time - elapsed_time) <=0 :
        game_result = "Time Over"
        running = False



    pygame.display.update()

# 게임오버 메세지
msg = game_font.render(game_result,True,(255,255,0)) #노란색
msg_rect = msg.get_rect(center = (int(screen_width/2),int(screen_height/2 )))
screen.blit(msg,msg_rect)
pygame.display.update() #이거 안하면 안 보임


pygame.time.delay(2000) #2초정도 대기하는 로직
pygame.quit()
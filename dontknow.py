#1차원 리스트의 각 원소 1줄로 출력하기
s = list(range(10))
print(s)
#기존
for i in s:
    print(i,end="")
#한줄로 
[i for i in s]

print()
print()

#join함수 설명
# 1.모양1 --> "".join(리스트)
# 모양2 --> "구분자".join(리스트)
# join함수는 매개변수로 들어온 리스트에 있는 요소 하나하나를 합쳐서 하나의 문자열로 바꾸어 변환하는 함수
# ''.join(리스트)를 이용하면 매개변수로 들어온 ['a', 'b', 'c'] 이런 식의 리스트를 'abc'의 문자열로 합쳐서 반환
# '_'.join(['a', 'b', 'c']) 라 하면 "a_b_c" 와 같은 형태로 문자열을 만들어서 반환

# join함수 예제1

a=['a','b','c','d','1','2','3']
print(a)
# 리스트를 문자열로 : join 이용
result1="".join(a)
print(result1)
# 리스트를 문자열로 : 하나하나 문자열을 더해서.
result2=''
for v in a:
    result2 +=v
print(result2)
print()
print()

# join함수 예제1
a=['BlockDMask','python','example','happy new year']
print(a)
# 리스트를 문자열로 합치기
result=".\n".join(a)
print(result)

#enumerate
list = ["가","나","다"]
for list_ind,list_val in enumerate(list):
    print(list_ind,list_val) #인덱스와 값을 가져와 줌



#이중 for문 탈출법
ball = [1,2,3,4]
weapon = [11,22,3,44]

for ball_idx,ball_val in enumerate(ball):
    print("ball : ",ball_val)
    for weapon_idx,weapon_val in enumerate(weapon):
        print("weapon :",weapon_val)
        if ball_val == weapon_val:
            print("collider!")
            break
    # for문에도 else를 쓸 수 있으며 for문이 더이상 반복되지 않는다면(weapon_val의 값이 없는 경우) 밑의 else문을 실행함
    #위의 break가 없다면 밑의 else문은 절대 실행X
    else:
        continue #그냥 이렇게 이중for문 탈출한다고 외우자....
    break #밖의 for문을 탈출하는 break 위의 break가 없다면 이 break를 탈 수 없음
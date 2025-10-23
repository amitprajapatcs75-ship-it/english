from itertools import product, permutations, combinations
# import datetime
# month, day, year = map(int,input().split())
# data = datetime.date(year, month, day)
# print(data.strftime("%A").upper())

#     n = int(input())
#     arr = map(int, input().split())
#     unique_score = list(set(arr))
#     unique_score.sort(reverse=True)
#     print(unique_score[1])

# A=list(map(int, input().split()))
# B=list(map(int, input().split()))
# for i in A:
#     for j in B:
#         print((i,j), end=" ")

# A = int(input("Enter first number:"))
# B = int(input("Enter second number:"))
# print(A//B)
# print(A/B)

# s, n = input().split()
# s = sorted(s)
# n=int(n)
# for i in range(n+1):
#     for c in combinations(s, n):
#         print("".join(c))

# s, n = input().split()
# n=int(n)
# for i in sorted(permutations(s, n)):
#         print("".join(i))

# import textwrap
#
# def wrap(string, max_width):
#     lines = textwrap.wrap(string, max_width)
#     return '\n'.join(lines)
#
# if __name__ == '__main__':
#     string, max_width = input(), int(input())
#     result = wrap(string, max_width)
#     print(result)

# s= input()
# has_alnum = False
# has_alpha = False
# has_digit = False
# has_lower = False
# has_upper = False
# for data in s:
#     if data.isalnum():
#         has_alnum = True
#     if data.isalpha():
#         has_alpha = True
#     if data.isdigit():
#         has_digit = True
#     if data.islower():
#         has_lower = True
#     if data.isupper():
#         has_upper = True
#
# print(has_alnum)
# print(has_alpha)
# print(has_digit)
# print(has_lower)
# print(has_upper)


# ----------------------------------------
# number = [1, 2, 3, 4]
# empty_number = []
# for num in number:
#     empty_number.append(num*num)
#     print(empty_number)

# number = [1, 2, 3, 4]
# square_number = list(map(lambda num: num*num, number))
# print(square_number)
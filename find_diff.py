
with open('Nasser history.txt', 'r') as user_1:
  with open('Mohammed history.txt', 'r') as user_2:
    with open('Ahmed history.txt', 'r') as user_3:
      user1_history = user_1.readlines()
      user2_history = user_2.readlines()
      user3_history = user_3.readlines()

      """ 
      we run the following depending on the current user

      if user 1 we check his history with the other users
      if user 2 we check his history with the other users
      .. and so on...
      """
      
      # this is just an example for performance we use other methods
      
      print('for user 1 with user 2')
      for item in list(set(user1_history) & set(user2_history)):
        if item not in user1_history:
          print(item)

      print('for user 1 with user 3')
      for item in list(set(user2_history) & set(user2_history)):
        if item not in user1_history:
          print(item)

      print('for user 2 with user 3')
      for item in list(set(user1_history) & set(user2_history)):
        if item not in user1_history:
          print(item)
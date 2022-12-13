# Movie recommendation system
## _To do list_
- [ ] Collabrative-based filtering algo. implementation:
    - The Algorithm to handle this filtering technique

- [ ] Prototype for the collabrative filtering for testing:
    - Add a dropdown list in the HTML for user simulation [user1, user2]
    - Add a button to run the algo. and generate the recommended movies

### _Completed tasks_
- [x] Content-based filtering
- [x] Prototype for the content filtering for testing
- [x] System simulation

## Filtering Techniques

### Content-based filtering 
- The recommendation system analyzes the past preferences of the user concerned, and then it uses this information to try to find similar movies. This information is available in the user history (Movie Genre). After that, the system provides movie recommendations for the user.

### Collabrative-based filtering 
- `User-based collaborative filtering` _Yet to be implemented_ The idea is to look for similar patterns in movie preferences in the target user and other users in the database.
- `Item-based collaborative filtering` _Not required in this system_ The basic concept here is to look for similar items (movies) that target users rate or interact with.

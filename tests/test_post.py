import unittest
from app import db
from app.models import User,Post

class PostModelTest(unittest.TestCase):
    def setup(self):
        self.user_Makena = User(username = 'Maryann',password = 'tomato', email = 'maks@gmail.com')
        
        self.new_post = Post(title='Interviews',post='I am going to talk about interview prep in this post.',user = self.user_Makena)

    def tearDown(self):
        Post.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_post.title,'Interviews')
        self.assertEquals(self.new_post.post,'I am going to talk about interview prep in this post.')
        self.assertEquals(self.new_post.user,self.user_Makena)

    def test_save_post(self):
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all())>0)    

    def test_get_post_by_id(self):
        self.new_post.save_post()
        got_post = Post.get_posts(2)
        self.assertTrue(len(got_post) == 1)
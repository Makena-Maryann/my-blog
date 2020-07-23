import unittest
from app import db
from app.models import User,Post,Comment

class CommentModelTest(unittest.TestCase):
    def setup(self):
        self.user_Makena = User(username = 'Maryann',password = 'tomato', email = 'maks@gmail.com')
        
        self.new_post = Post(title='Interviews',post='I am qualified',user = self.user_Makena)

        self.new_comment = Comment(post_comment='Awesome',post=self.new_post,user=self.user_Makena)

    def tearDown(self):
        Comment.query.delete()
        Post.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.post_comment,'Awesome')
        self.assertEquals(self.new_comment.post,self.new_post)
        self.assertEquals(self.new_comment.user,self.user_Makena)

    def test_save_pitch(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)    

    def test_get_comments(self):
        self.new_comment.save_comment()
        got_comments = Post.get_comments(2)
        self.assertTrue(len(got_comments) > 1)

        
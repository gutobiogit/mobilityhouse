# import unittest
# from unittest import mock
 
# class Test_PV(unittest.TestCase):
 

    # @mock.patch(f'{__name__}1.foo', autospec=True, side_effect=parse_magic("13:22:18"))
    # def test_foo_return_and_local_params_values(self, mocked):
        # self.assertEqual( mocked.side_effect.design_name,'3246.8') #PASS

    # @mock.patch(f'{__name__}1.foo', autospec=True, side_effect=parse_magic("20:04:03"))
    # def test_foo_return_and_local_params_values(self, mocked):
        # self.assertEqual(mocked.side_effect.design_name,'278.9') #PASS
 
    # @mock.patch(f'{__name__}1.foo', autospec=True, side_effect=parse_magic("01:20:25"))
    # def test_foo_return_and_local_params_values(self, mocked):
        # self.assertEqual( mocked.side_effect.design_name,'0.0') #PASS


    # @mock.patch(f'{__name__}1.foo', autospec=True, side_effect=getdata())
    # def test_foo_return_and_local_params_values(self, mocked):
        #time_now=datetime.now()
        #new.append(1055)
        #new.append(time_now)
        #new.append(3246.8)
        # self.assertEqual(mocked.side_effect.design_name,[1055,datetime.now(),3246.8]) #PASS

    # @mock.patch(f'{__name__}1.foo', autospec=True, side_effect=getdata())
    # def test_foo_return_and_local_params_values(self, mocked):
        #time_now=datetime.now()
        #new.append(8600)
        #new.append(time_now)
        #new.append(278.9)
        # self.assertEqual(mocked.side_effect.design_name,[8600,datetime.now(),278.9]) #PASS

    # @mock.patch(f'{__name__}1.foo', autospec=True, side_effect=getdata())
    # def test_foo_return_and_local_params_values(self, mocked):
        #time_now=datetime.now()
        #new.append(0)
        #new.append(time_now)
        #new.append(0.0)
        # self.assertEqual(mocked.side_effect.design_name,[0.0,datetime.now(),0.0]) #PASS

import pytest

from ecommerce.user.models import User

@pytest.fixure(autouse=True)
def create_dummy_user(tmpdir):
    """Fixure to execute asserts before and after a test is run"""
    
    from conf_test_db import override_get_db
    database = next(override_get_db())
    new_user = User(name="Testname", email="test@gmail.com", password="Test1234")
    database.add(new_user)
    database.commit()
    
    yield # this is where the testing happens
    
    # teardown
    database.query(User).filter(User.email == 'test@gmail.com').delete()
    database.commit()
    
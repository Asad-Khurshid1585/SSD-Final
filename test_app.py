import pytest
from app import app, db, User
import os


@pytest.fixture
def client():
    """Create a test client with a temporary database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_user(client):
    """Create a sample user for testing."""
    with app.app_context():
        user = User(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            age=30,
            city='New York'
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    return user_id


class TestUserModel:
    """Test the User model."""
    
    def test_user_creation(self):
        """Test creating a user."""
        with app.app_context():
            db.create_all()
            user = User(
                first_name='Jane',
                last_name='Smith',
                email='jane@example.com',
                age=25,
                city='Los Angeles'
            )
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.first_name == 'Jane'
            assert user.last_name == 'Smith'
            assert user.email == 'jane@example.com'
            assert user.age == 25
            assert user.city == 'Los Angeles'
    
    def test_user_repr(self, sample_user):
        """Test user string representation."""
        with app.app_context():
            user = User.query.get(sample_user)
            assert repr(user) == f"<User {user.id} John>"


class TestRoutes:
    """Test Flask routes."""
    
    def test_index_route(self, client):
        """Test the index route returns a 200 status."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_displays_users(self, client, sample_user):
        """Test that index displays users."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'John' in response.data
        assert b'Doe' in response.data
    
    def test_add_user_post(self, client):
        """Test adding a user via POST request."""
        response = client.post('/add', data={
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'email': 'alice@example.com',
            'age': '28',
            'city': 'Chicago'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        with app.app_context():
            user = User.query.filter_by(email='alice@example.com').first()
            assert user is not None
            assert user.first_name == 'Alice'
            assert user.last_name == 'Johnson'
            assert user.age == 28
            assert user.city == 'Chicago'
    
    def test_delete_user(self, client, sample_user):
        """Test deleting a user."""
        user_id = sample_user
        
        response = client.get(f'/delete/{user_id}', follow_redirects=True)
        assert response.status_code == 200
        
        with app.app_context():
            user = User.query.get(user_id)
            assert user is None
    
    def test_delete_nonexistent_user(self, client):
        """Test deleting a non-existent user returns 404."""
        response = client.get('/delete/999')
        assert response.status_code == 404
    
    def test_update_user_get(self, client, sample_user):
        """Test GET request to update user form."""
        user_id = sample_user
        
        response = client.get(f'/update/{user_id}')
        assert response.status_code == 200
    
    def test_update_user_post(self, client, sample_user):
        """Test updating a user via POST request."""
        user_id = sample_user
        
        response = client.post(f'/update/{user_id}', data={
            'first_name': 'Jonathan',
            'last_name': 'Smith',
            'email': 'jonathan@example.com',
            'age': '35',
            'city': 'Boston'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        with app.app_context():
            user = User.query.get(user_id)
            assert user.first_name == 'Jonathan'
            assert user.last_name == 'Smith'
            assert user.email == 'jonathan@example.com'
            assert user.age == 35
            assert user.city == 'Boston'
    
    def test_update_nonexistent_user(self, client):
        """Test updating a non-existent user returns 404."""
        response = client.get('/update/999')
        assert response.status_code == 404


class TestDataValidation:
    """Test data validation and constraints."""
    
    def test_unique_email_constraint(self, client, sample_user):
        """Test that email must be unique."""
        with app.app_context():
            duplicate_user = User(
                first_name='Duplicate',
                last_name='User',
                email='john@example.com',
                age=25,
                city='San Francisco'
            )
            db.session.add(duplicate_user)
            
            with pytest.raises(Exception):
                db.session.commit()
    
    def test_required_fields(self, client):
        """Test that required fields cannot be null."""
        with app.app_context():
            user = User(
                first_name='Test',
                last_name='User',
                # Missing email
                age=25,
                city='Test City'
            )
            db.session.add(user)
            
            with pytest.raises(Exception):
                db.session.commit()

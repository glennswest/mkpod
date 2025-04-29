import psycopg2
from sqlalchemy import create_engine, text,  Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
import os
from datetime import datetime
from pydantic import PostgresDsn
from sqlalchemy.exc import OperationalError


Base = declarative_base()

class Container(Base):
    __tablename__ = 'containers'
    
    id = Column(Integer, primary_key=True)
    container_id = Column(String(64), unique=True, nullable=False)
    name = Column(String(255))
    created = Column(DateTime)
    state = Column(JSON)  # PostgreSQL JSONB type
    image_name = Column(String(255))
    config = Column(JSON)  # PostgreSQL JSONB type
    host_config = Column(JSON)  # PostgreSQL JSONB type
    network_settings = Column(JSON)  # PostgreSQL JSONB type
    
def create_database():
    # Get database connection details from environment variables for security
    db_user = os.environ.get('DB_USER', 'postgres')
    db_password = os.environ.get('DB_PASSWORD','PASSWORD')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5433')
    db_name = os.environ.get('DB_NAME', 'poddb')
    
    # Create PostgreSQL database connection URL
    my_database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    base_database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
    print({db_name})
    # Create engine with PostgreSQL-specific parameters
    engine = create_engine(
            base_database_url,
            echo=False,  # Set to True for SQL query logging
            pool_size=5,  # Connection pool size
            max_overflow=10,  # Maximum overflow connections
            pool_timeout=30,  # Timeout for getting connection from pool
            pool_recycle=1800,  # Recycle connections after 30 minutes
            )
    if not database_exists(my_database_url):
        print("Creating database")
        engine = create_engine(
              base_database_url,
              echo=False,  # Set to True for SQL query logging
              pool_size=5,  # Connection pool size
              max_overflow=10,  # Maximum overflow connections
              pool_timeout=30,  # Timeout for getting connection from pool
              pool_recycle=1800,  # Recycle connections after 30 minutes
              )
        conn = engine.connect()
        query = text("COMMIT")
        conn.execute(query)
        query = text("CREATE DATABASE " + db_name)
        conn.execute(query)
        print(f"Database {db_name} created")
        print("Creating tables")
        # Create all tables
        Base.metadata.create_all(engine)
    print("Creating Session")
    # Create session factory
    Session = sessionmaker(bind=engine)
    print(engine)
    print(Session)
        
    print("All done")
    return engine, Session

def store_container_data(session, container_data):
    """
    Store container data in the PostgreSQL database
    
    Args:
        session: SQLAlchemy session
        container_data: Dictionary containing container information
    """
    try:
        # Convert the created timestamp string to datetime object
        created_time = datetime.fromisoformat(container_data['Created'].replace('Z', '+00:00'))
        
        container = Container(
            container_id=container_data['Id'],
            name=container_data['Name'],
            created=created_time,
            state=container_data['State'],
            image_name=container_data['ImageName'],
            config=container_data['Config'],
            host_config=container_data['HostConfig'],
            network_settings=container_data['NetworkSettings']
        )
        
        # Check if container already exists
        existing_container = session.query(Container).filter_by(
            container_id=container_data['Id']
        ).first()
        
        if existing_container:
            # Update existing container
            for key, value in container.__dict__.items():
                if not key.startswith('_'):
                    setattr(existing_container, key, value)
        else:
            # Add new container
            session.add(container)
            
        session.commit()
        
    except Exception as e:
        session.rollback()
        print(f"Error storing container data: {str(e)}")
        raise

def get_container_by_id(session, container_id):
    """
    Retrieve container data from the PostgreSQL database by container ID
    
    Args:
        session: SQLAlchemy session
        container_id: The container ID to search for
        
    Returns:
        Container: Container object if found
        None: If no container is found with the given ID
        
    Raises:
        Exception: If there's an error during the database query
    """
    try:
        container = session.query(Container).filter_by(container_id=container_id).first()
        
        if container:
            return {
                'id': container.id,
                'container_id': container.container_id,
                'name': container.name,
                'created': container.created.isoformat(),
                'state': container.state,
                'image_name': container.image_name,
                'config': container.config,
                'host_config': container.host_config,
                'network_settings': container.network_settings
            }
        return None
        
    except Exception as e:
        print(f"Error retrieving container data: {str(e)}")
        raise

# Example usage:
if __name__ == "__main__":
    engine, Session = create_database()
    session = Session()
    
    try:
        # Example container ID
        container_id = "99f66530fe9c7249f7cf29f78e8661669d5831cbe4ee80ea757d5e922dd6a8a6"
        
        # Get container data
        container = get_container_by_id(session, container_id)
        
        if container:
            print("Container found:")
            print(f"Name: {container['name']}")
            print(f"Image: {container['image_name']}")
            print(f"State: {container['state']}")
        else:
            print(f"No container found with ID: {container_id}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        session.close()

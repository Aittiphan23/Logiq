"""
Unit tests for database manager
"""

import pytest
import asyncio
from database.db_manager import DatabaseManager
from database.models import User, Guild


@pytest.fixture
async def db_manager():
    """Create database manager for testing"""
    db = DatabaseManager("mongodb://localhost:27017", "Logiq_test", pool_size=5)
    await db.connect()
    yield db
    await db.disconnect()


@pytest.mark.asyncio
async def test_user_creation(db_manager):
    """Test user creation"""
    user_id = 123456789
    guild_id = 987654321

    user = await db_manager.create_user(user_id, guild_id)
    assert user['user_id'] == user_id
    assert user['guild_id'] == guild_id
    assert user['balance'] == 1000
    assert user['xp'] == 0
    assert user['level'] == 0


@pytest.mark.asyncio
async def test_user_retrieval(db_manager):
    """Test user retrieval"""
    user_id = 123456789
    guild_id = 987654321

    await db_manager.create_user(user_id, guild_id)
    retrieved = await db_manager.get_user(user_id, guild_id)

    assert retrieved is not None
    assert retrieved['user_id'] == user_id


@pytest.mark.asyncio
async def test_balance_operations(db_manager):
    """Test balance add/remove"""
    user_id = 123456789
    guild_id = 987654321

    await db_manager.create_user(user_id, guild_id)

    # Add balance
    await db_manager.add_balance(user_id, guild_id, 500)
    user = await db_manager.get_user(user_id, guild_id)
    assert user['balance'] == 1500

    # Remove balance
    await db_manager.remove_balance(user_id, guild_id, 300)
    user = await db_manager.get_user(user_id, guild_id)
    assert user['balance'] == 1200


@pytest.mark.asyncio
async def test_guild_creation(db_manager):
    """Test guild creation"""
    guild_id = 987654321

    guild = await db_manager.create_guild(guild_id)
    assert guild['guild_id'] == guild_id
    assert guild['prefix'] == "/"


@pytest.mark.asyncio
async def test_leaderboard(db_manager):
    """Test leaderboard retrieval"""
    guild_id = 987654321

    # Create multiple users with different XP
    for i in range(5):
        await db_manager.create_user(100 + i, guild_id, {"xp": (i + 1) * 100})

    leaderboard = await db_manager.get_leaderboard(guild_id, limit=5)
    assert len(leaderboard) == 5
    assert leaderboard[0]['xp'] > leaderboard[-1]['xp']  # Should be sorted


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

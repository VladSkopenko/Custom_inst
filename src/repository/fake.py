from faker import Faker

fake = Faker("en")


def get_fake_user():
    interests = [fake.word() for _ in range(3)]
    fake_user = {
        "id": fake.random_digit(),
        "username": fake.user_name(),
        "description": f"I enjoy {', '.join(interests)} and believes that {fake.catch_phrase()}.",
        "avatarUrl": fake.image_url(),
        "subscriptionsAmount": fake.random_digit(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "isActive": fake.boolean(),
        "stack": [fake.word() for _ in range(5)],
        "city": fake.city(),
    }
    return fake_user


async def create_fake_user():
    result = [get_fake_user() for _ in range(0, 5)]
    return result


async def create_fake_followers():
    fake_follower = {
        "items": await create_fake_user(),
        "total": 15,
        "page": 3,
        "size": 5,
        "pages": 1,
    }
    return fake_follower

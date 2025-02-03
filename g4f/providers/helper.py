from __future__ import annotations

import random
import string

from ..typing import Messages, Cookies, AsyncIterator, Iterator
from .. import debug

def format_prompt(messages: Messages, add_special_tokens: bool = False, do_continue: bool = False) -> str:
    """
    Format a series of messages into a single string, optionally adding special tokens.

    Args:
        messages (Messages): A list of message dictionaries, each containing 'role' and 'content'.
        add_special_tokens (bool): Whether to add special formatting tokens.

    Returns:
        str: A formatted string containing all messages.
    """
    if not add_special_tokens and len(messages) <= 1:
        return messages[0]["content"]
    formatted = "\n".join([
        f'{message["role"].capitalize()}: {message["content"]}'
        for message in messages
    ])
    if do_continue:
        return formatted
    return f"{formatted}\nAssistant:"


def format_alternating_prompt(messages: Messages) -> Messages:
    formatted_messages: Messages = []
    current_role: str | None = None
    current_content: str = ""
    system_prompt: str | None = None

    for message in messages:
        role = message["role"]
        content = message["content"]

        if role == "system":
            system_prompt = content
            continue

        if role != current_role:
            if current_role is not None:
                formatted_messages.append({"role": current_role, "content": current_content})
            current_role = role
            current_content = content
        else:
            current_content += "\n" + content

    if current_role is not None:
        formatted_messages.append({"role": current_role, "content": current_content})

    if not formatted_messages or formatted_messages[0]["role"] != "user":
        formatted_messages.insert(0, {"role": "user", "content": ""})

    if system_prompt:
        formatted_messages[0]["content"] = system_prompt + "\n" + formatted_messages[0]["content"]

    if formatted_messages[-1]["role"] != "user":
        formatted_messages.append({"role": "user", "content": ""})

    return formatted_messages

def get_last_user_message(messages: Messages) -> str:
    user_messages = []
    last_message = None if len(messages) == 0 else messages[-1]
    while last_message is not None and messages:
        last_message = messages.pop()
        if last_message["role"] == "user":
            if isinstance(last_message["content"], str):
                user_messages.append(last_message["content"].strip())
        else:
            return "\n".join(user_messages[::-1])
    return "\n".join(user_messages[::-1])

def format_image_prompt(messages, prompt: str = None) -> str:
    if prompt is None:
        return get_last_user_message(messages)
    return prompt

def format_prompt_max_length(messages: Messages, max_lenght: int) -> str:
    prompt = format_prompt(messages)
    start = len(prompt)
    if start > max_lenght:
        if len(messages) > 6:
            prompt = format_prompt(messages[:3] + messages[-3:])
        if len(prompt) > max_lenght:
            if len(messages) > 2:
                prompt = format_prompt([m for m in messages if m["role"] == "system"] + messages[-1:])
            if len(prompt) > max_lenght:
                prompt = messages[-1]["content"]
        debug.log(f"Messages trimmed from: {start} to: {len(prompt)}")
    return prompt

def get_random_string(length: int = 10) -> str:
    """
    Generate a random string of specified length, containing lowercase letters and digits.

    Args:
        length (int, optional): Length of the random string to generate. Defaults to 10.

    Returns:
        str: A random string of the specified length.
    """
    return ''.join(
        random.choice(string.ascii_lowercase + string.digits)
        for _ in range(length)
    )


def get_random_hex(length: int = 32) -> str:
    """
    Generate a random hexadecimal string with n length.

    Returns:
        str: A random hexadecimal string of n characters.
    """
    return ''.join(
        random.choice("abcdef" + string.digits)
        for _ in range(length)
    )


def filter_none(**kwargs) -> dict:
    return {
        key: value
        for key, value in kwargs.items()
        if value is not None
    }

async def async_concat_chunks(chunks: AsyncIterator) -> str:
    return concat_chunks([chunk async for chunk in chunks])

def concat_chunks(chunks: Iterator) -> str:
    return "".join([
        str(chunk) for chunk in chunks
        if chunk and not isinstance(chunk, Exception)
    ])

def format_cookies(cookies: Cookies) -> str:
    return "; ".join([f"{k}={v}" for k, v in cookies.items()])


first_names = [
    # Western names
    "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason",
    "Isabella", "William", "Mia", "James", "Charlotte", "Benjamin", "Amelia",
    "Oliver", "Evelyn", "Elijah", "Abigail", "Lucas", "Harper", "Alexander",
    # Hispanic names
    "Sofia", "Mateo", "Camila", "Sebastian", "Isabella", "Diego", "Valentina",
    "Emiliano", "Lucia", "Santiago", "Valeria", "Alejandro", "Ximena", "Leonardo",
    # Asian names
    "Yuki", "Hiroshi", "Mei", "Zhang", "Li", "Wei", "Soo-yun", "Ji-hun",
    "Akira", "Hana", "Ryu", "Yuna", "Kazuki", "Eun-ji", "Kenji", "Sakura",
    # African names
    "Kwame", "Amara", "Chidi", "Zalika", "Tendai", "Akinyi", "Oluwaseun",
    "Kofi", "Zuri", "Oluwadamilola", "Imani", "Nnamdi", "Thando", "Abimbola",
    # Middle Eastern names
    "Fatima", "Mohammed", "Zara", "Ahmed", "Layla", "Hassan", "Amira",
    "Yusuf", "Noor", "Ali", "Rania", "Omar", "Yasmin", "Karim", "Leila",
    # Indian names
    "Aarav", "Priya", "Arjun", "Divya", "Ravi", "Neha", "Vikram",
    "Aisha", "Rohan", "Anaya", "Kiran", "Aditi", "Vihaan", "Zoya", "Arnav"
]

last_names = [
    # Western names
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    # Asian names
    "Zhang", "Wang", "Li", "Chen", "Liu", "Yang", "Huang", "Kim", "Lee", "Park",
    "Nakamura", "Tanaka", "Suzuki", "Sato", "Watanabe", "Takahashi", "Yamamoto",
    # African names
    "Okafor", "Mwangi", "Afolayan", "Okonkwo", "Nwosu", "Mensah", "Okoro",
    "Adebayo", "Osei", "Ngozi", "Dube", "Eze", "Khumalo", "Moyo", "Nkosi",
    # Middle Eastern names
    "Al-Fahad", "El-Masri", "Sayegh", "Haddad", "Najjar", "Khalil", "Zidan",
    "Abboud", "Hakim", "Saleh", "Fares", "Nassar", "Sabbagh", "Yousef",
    # Indian names
    "Patel", "Singh", "Kumar", "Shah", "Sharma", "Reddy", "Gupta", "Kapoor",
    "Malhotra", "Joshi", "Chopra", "Mehra", "Verma", "Desai", "Banerjee", "Das"
]

middle_names = [
    "Rose", "James", "Marie", "John", "Elizabeth", "Michael", "Anne", "William",
    "Grace", "Thomas", "May", "Lee", "Jane", "Robert", "Lynn", "David", "Joy",
    "Alexis", "Jade", "Ray", "Sky", "Quinn", "Sage", "Kai", "Wren", "Finn"
]


def generate_random_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    # 30% chance to use a middle name
    if random.random() < 0.3:
        middle_name = random.choice(middle_names)
        full_name = f"{first_name} {middle_name} {last_name}"
    else:
        full_name = f"{first_name} {last_name}"

    # 50% chance to separate names with a dot
    if random.random() < 0.5:
        full_name = full_name.replace(" ", ".")
    else:
        full_name = full_name.replace(" ", "")

    # 75% chance to either append a small number (1-20) or a year of birth (1950-2006)
    if random.random() < 0.75:
        a = random.random()
        if a < 0.33:
            full_name += str(random.randint(1, 20))
        elif a < 0.66:
            full_name += str(random.randint(1950, 2006))[2:]
        else:
            full_name += str(random.randint(1950, 2006))

    return full_name.lower()

## Telegram Bot for Managing Subscriptions to Sponsor Channels

This bot is designed to automate the process of managing user subscriptions to sponsor channels on Telegram. It checks users' subscriptions, sends warnings in case of missing subscriptions to required channels, and allows users to subscribe to the missing channels. If a user does not confirm their subscription within a set time frame, the bot removes them from the target channel.

# Key Features

1. Granting access to a closed channel to users who meet certain conditions.

2. Regular subscription checks: The bot periodically checks users' subscriptions to the target sponsor channel.

3. Warning notifications: In case of missing subscriptions to any sponsor channel, the bot sends a warning to the user with links to the missing channels.

4. Subscription confirmation: Users can confirm their subscription by clicking the "I SUBSCRIBED" button in the bot's message.

5. User exclusion: If a user does not confirm their subscription within the set time frame, the bot removes them from the target sponsor channels.

6. User database management: The bot stores user information in a database to manage their subscriptions and exclusions.

# How to Use

1. Configure the necessary settings in the files in the "templates" folder.

2. Add your bot token to the .env file.

3. Install the required dependencies: Open a command prompt or terminal in the project directory and run the following command:
    ```bash
    pip install -r requirements.txt
    ```

4. Start the bot from the project directory:
    ```bash
    python bot.py
    ```

# Dependencies

aiogram==3.0.0

APScheduler==3.10.4

loguru==0.7.2

python-dotenv==1.0.0
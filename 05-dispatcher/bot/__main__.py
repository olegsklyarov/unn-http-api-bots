import bot.long_polling


def main() -> None:
    try:
        bot.long_polling.start_long_polling()
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()

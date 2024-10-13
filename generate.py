import argparse
import content_generation


def main():
    parser = argparse.ArgumentParser(
        description="Generate content using AI for different platforms"
    )

    subparsers = parser.add_subparsers(
        title="Types",
        description="Type of content to generate",
        dest="type",
        required=True,
    )

    ##### Subparser for 'podcast' #####
    podcast_parser = subparsers.add_parser("podcast", help="Generate a podcast episode")
    podcast_parser.add_argument(
        "--description", type=str, required=True, help="Description of the episode"
    )

    ##############################

    args = parser.parse_args()

    module = getattr(content_generation, args.type.title())

    # Convert parsed arguments to kwargs
    kwargs = vars(args)  # This converts Namespace to a dictionary

    module().run(**kwargs)


if __name__ == "__main__":
    main()

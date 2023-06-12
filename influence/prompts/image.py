IMAGE_PROMPT = '''
I want you to act as a prompt generator for DALL-E 2's artificial intelligence program. You will read the given quote and provide detailed and creative descriptions that will inspire unique and interesting images from the AI that would perfectly compliment the given quote. You'll not mention about the quote in the description. Keep in mind that the AI is capable of understanding a wide range of language and can interpret abstract concepts, so feel free to be as imaginative and descriptive as possible. Try to visualize the given quote. The more detailed and imaginative your description, the more interesting the resulting image will be. 

Below are the things you have to keep in mind while building the description:
1) Keep it simple stupid, Build your subject first, as detailed as possible.
2) Specify an Art Style. You could mention Cyberpunk, 3D, Realistic, Retro/vintage, Geometric, Vector, Flat art, Surrealism, Psychedelic etc.. Whatever that fits the given quote's mood.
3) Don't Forget About the Background (For example, A grasshopper superhero action figure being held by a kid)
4) Specify camera angles and details (For example, A 35 mm macro shot of a cat with glasses)
5) Specify lighting details (For example, An elephant eating sugarcane at the sunrise)
6) Keep the description within 150 words

Return only the description without any headers. Here is your first quote:

{quote}'''
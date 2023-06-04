def format_quotes(q_list):
    fquotes = ""
    for i,l in enumerate(q_list, 1):
        fquotes+=f"{i}) {l}\n"
    return fquotes
def get_first_error(form):
    if form.errors:
        return list(form.errors.values())[0][0]
    else:
        return ""

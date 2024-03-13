def handle_form_data(form_data):
    try:
        # the number of series
        nombre_series = int(form_data.get("nombre_series"))
        if nombre_series < 1:
            raise ValueError("Le nombre de séries doit être un entier positif.")

        # the number of exercises per series
        nombre_exercices = int(form_data.get("nombre_exercices"))
        if nombre_exercices < 1:
            raise ValueError(
                "Le nombre d'exercices par série doit être un entier positif."
            )

        # the duration of each exercise (in seconds)
        temps_travail_par_exercice = int(form_data.get("temps_travail_par_exercice"))
        if temps_travail_par_exercice < 1:
            raise ValueError("La durée de chaque exercice doit être un entier positif.")

        # the rest time between exercises (in seconds)
        temps_repos_exercices = int(form_data.get("temps_repos_exercices"))
        if temps_repos_exercices < 0:
            raise ValueError(
                "Le temps de repos entre les exercices doit être un entier non négatif."
            )

        # the rest time between series (in seconds)
        temps_repos_series = int(form_data.get("temps_repos_series"))
        if temps_repos_series < 1:
            raise ValueError(
                "Le temps de repos entre les séries doit être un entier positif."
            )
        return (
            nombre_series,
            nombre_exercices,
            temps_travail_par_exercice,
            temps_repos_exercices,
            temps_repos_series,
        )
    except ValueError as error:
        print("error while extracting form data: ", error)
        return None, None, None, None, None

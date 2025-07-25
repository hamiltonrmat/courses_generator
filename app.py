import streamlit as st
import openai

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Générateur de Cours SkillQuest",
    page_icon="⚔️",
    layout="wide"
)

# --- Fonctions ---

def build_prompt(domaine, competence, titre_cours, mots_cles, structure):
    """
    Construit le prompt détaillé pour l'API OpenAI en intégrant la philosophie SkillQuest.
    C'est la partie la plus importante : on donne son rôle et ses instructions au modèle.
    """
    
    # Message système pour donner le contexte et le rôle à l'IA
    system_prompt = """
    Tu es un concepteur pédagogique expert, spécialisé dans la gamification et la création de contenu pour le dispositif innovant "SkillQuest" à UniLaSalle.
    Ta mission est de rédiger une trame de cours complète en format Markdown, destinée à être utilisée dans Obsidian et publiée via Obsidian Publish.
    Le public cible sont les étudiants en cycle Pré-Ingénieur, appelés "joueurs".
    Le ton doit être immersif, engageant et motivant, transformant l'apprentissage en une véritable quête.
    """

    # Instructions détaillées pour l'utilisateur (le "joueur")
    user_prompt = f"""
    Rédige un cours structuré comme une "Quête" sur le sujet suivant.

    **Informations sur la Quête :**
    - **Domaine :** {domaine}
    - **Compétence à valider :** {competence}
    - **Titre de la Quête (du cours) :** {titre_cours}
    - **Mots-clés pour l'orientation :** {mots_cles}

    **Structure Suggérée (si fournie) :**
    {structure if structure else "Le joueur n'a pas fourni de structure, tu es libre de proposer la plus pertinente."}

    **Directives de Formatage et de Contenu (TRÈS IMPORTANT) :**

    1.  **Format Markdown pour Obsidian :** Utilise intensivement le Markdown :
        - Titres (`#`, `##`, `###`). Le titre principal doit commencer par `# ⚔️ Quête : {titre_cours}`.
        - Listes à puces (`-` ou `*`).
        - Texte en gras (`**texte**`) et italique (`*texte*`).
        - Blocs de citation (`>`) pour les conseils du "Guide" ou les points importants.
        - Blocs de code (```) pour les exemples mathématiques ou de code.
        - Liens internes Obsidian `[[Nom d'une autre note]]` si tu penses à des concepts liés.

    2.  **Intégration de la Gamification SkillQuest :**
        - **Introduction ("Briefing de la Quête") :** Présente le contexte, l'intérêt de la quête et ce que le "joueur" va découvrir.
        - **Objectifs :** Liste clairement les objectifs d'apprentissage. "À la fin de cette quête, tu seras capable de...".
        - **Prérequis :** Mentionne les compétences ou quêtes préalables nécessaires.
        - **Récompenses :** Indique les XP (Points d'Expérience) potentiels à gagner pour la validation de la compétence. Mentionne les niveaux de récompense : **Bronze**, **Argent**, **OR**.
        - **Corps du cours ("Les Étapes de la Quête") :** Divise le contenu en sections logiques. Chaque section peut être une étape.
        - **Intégrer les "Défis" :** À la fin du cours, propose une section `### 🚀 Tes Défis pour Valider la Compétence` qui liste les différentes manières de valider la compétence, en utilisant la terminologie SkillQuest :
            - **Défi "Conférence" :** "Assimiler les connaissances présentées dans cette quête."
            - **Défi "Atelier" :** Propose 2-3 exercices pratiques pour appliquer les notions.
            - **Défi "Autonomie" :** Suggère des problèmes plus complexes ou des ressources externes à explorer seul.
            - **Défi "Tutorat" :** "Prends rendez-vous avec un 'Guide' pour éclaircir un point précis."
            - **Défi "Examen" :** "Lorsque tu te sens prêt, inscris-toi à l'examen pour valider cette compétence et remporter tes XP !".
        - **Conclusion ("Débriefing de la Quête") :** Fais un résumé rapide et encourage le joueur pour la suite de son aventure.
        - **Aller plus loin ("Quêtes Annexes") :** Propose des pistes pour des projets ou des "Quêtes du Diamant" en lien avec le sujet.

    3.  **Ton et Langage :**
        - Adresse-toi directement au "joueur" en utilisant "tu" ou "vous".
        - Utilise un vocabulaire épique et ludique : "aventure", "maîtriser", "explorer", "artefact" (pour un théorème clé), etc.
        - Intègre des emojis pertinents (⚔️, 🎯, 💡, 🏆, 🚀, 📚) pour rendre le texte plus vivant.

    Génère maintenant le cours en Markdown en suivant scrupuleusement ces instructions.
    """
    
    return system_prompt, user_prompt

def generate_course(api_key, domaine, competence, titre_cours, mots_cles, structure):
    """
    Appelle l'API OpenAI pour générer le contenu du cours.
    """
    try:
        openai.api_key = api_key
        system_prompt, user_prompt = build_prompt(domaine, competence, titre_cours, mots_cles, structure)
        
        response = openai.chat.completions.create(
            model="gpt-4o", # Ou "gpt-3.5-turbo" pour une option plus rapide et moins coûteuse
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7, # Un peu de créativité mais reste factuel
            max_tokens=3000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Une erreur est survenue lors de l'appel à l'API OpenAI : {e}")
        return None

# --- Interface Streamlit ---

st.title("⚔️ Générateur de Contenu SkillQuest")
st.markdown("Cet outil vous aide à créer des contenus de cours au format Markdown, parfaitement intégrés à la philosophie **SkillQuest**. Le résultat est optimisé pour [Obsidian](https://obsidian.md/).")

# --- Panneau latéral pour la configuration ---
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("Entrez votre clé API OpenAI", type="password")
    st.markdown("---")
    st.header("📖 Contexte SkillQuest")
    st.info("Cette application s'appuie sur le document de cadrage de SkillQuest pour générer des contenus pédagogiques gamifiés et engageants.")
    st.image("https://www.unilasalle.fr/sites/default/files/styles/logo/public/2022-12/logo-unilasalle_0.png?itok=36nOaG5c") # Vous pouvez changer l'URL par un logo local si vous le souhaitez

# --- Formulaire principal ---
st.header("🎯 Définissez votre Quête Pédagogique")

if not api_key:
    st.warning("Veuillez entrer votre clé API OpenAI dans le panneau latéral pour commencer.")
else:
    with st.form("course_form"):
        col1, col2 = st.columns(2)
        with col1:
            domaine = st.text_input("Domaine", "Mathématiques Numériques", help="Ex: Physique, Chimie, Informatique...")
            competence = st.text_input("Compétence à valider", "Primitives et Intégrales", help="La compétence que le joueur doit acquérir.")
        
        with col2:
            titre_cours = st.text_input("Titre du cours (de la Quête)", "L'intégration par parties", help="Le nom de la quête.")
            mots_cles = st.text_input("Mots-clés", "calcul intégral, intégration, fonctions, analyse", help="Séparés par des virgules.")

        structure = st.text_area(
            "Structure du cours (optionnel)",
            placeholder="Exemple:\n1. Introduction : À quoi ça sert ?\n2. La formule magique et sa démonstration\n3. Exemples guidés pas à pas\n4. Pièges à éviter et cas particuliers\n5. Application concrète",
            height=150,
            help="Indiquez les chapitres ou sections que vous souhaitez voir apparaître. Laissez vide pour laisser l'IA décider."
        )

        submitted = st.form_submit_button("✨ Générer la Quête ✨", use_container_width=True)

    if submitted:
        with st.spinner("Votre 'Guide' IA est en train de forger votre quête... Veuillez patienter..."):
            generated_content = generate_course(api_key, domaine, competence, titre_cours, mots_cles, structure)
        
        if generated_content:
            st.session_state['generated_content'] = generated_content

    # Afficher le contenu s'il existe dans l'état de la session
    if 'generated_content' in st.session_state:
        st.header("✅ Votre Quête est prête !")
        st.markdown("---")

        st.subheader("Aperçu du cours")
        st.markdown(st.session_state['generated_content'])
        st.markdown("---")

        st.subheader("Code Markdown à copier dans Obsidian")
        st.info("Cliquez sur l'icône de copie en haut à droite du bloc de code ci-dessous, puis collez directement dans une nouvelle note Obsidian.")
        st.code(st.session_state['generated_content'], language='markdown')

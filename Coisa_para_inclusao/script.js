// Lógica do aplicativo Mobile
console.log("App de Rotina Inclusiva iniciado!");

const translations = {
    "en": {
        "morning_route": "Morning Route",
        "hi_leo": "Hi, Leo! 👋",
        "todays_adventure": "Today's Adventure",
        "tasks_count": "8 Tasks",
        "task_circle_time": "Circle Time",
        "task_wash_hands": "Wash Hands",
        "task_brush_teeth": "Brush Teeth",
        "task_snack_time": "Snack Time",
        "task_play_time": "Play Time",
        "task_park_trip": "Park Trip",
        "task_lunch": "Lunch",
        "task_go_home": "Go Home",
        "tap_to_speak": "Tap to Speak",
        "nav_home": "Home",
        "nav_plan": "Plan",
        "nav_rewards": "Rewards",
        "nav_profile": "Profile"
    },
    "pt": {
        "morning_route": "Rotina Matinal",
        "hi_leo": "Oi, Leo! 👋",
        "todays_adventure": "Aventura de Hoje",
        "tasks_count": "8 Tarefas",
        "task_circle_time": "Roda de Conversa",
        "task_wash_hands": "Lavar as Mãos",
        "task_brush_teeth": "Escovar os Dentes",
        "task_snack_time": "Hora do Lanche",
        "task_play_time": "Hora de Brincar",
        "task_park_trip": "Passeio no Parque",
        "task_lunch": "Almoço",
        "task_go_home": "Ir para Casa",
        "tap_to_speak": "Toque para Falar",
        "nav_home": "Início",
        "nav_plan": "Plano",
        "nav_rewards": "Prêmios",
        "nav_profile": "Perfil"
    },
    "es": {
        "morning_route": "Rutina Matutina",
        "hi_leo": "¡Hola, Leo! 👋",
        "todays_adventure": "Aventura de Hoy",
        "tasks_count": "8 Tareas",
        "task_circle_time": "Círculo de Charla",
        "task_wash_hands": "Lavarse las Manos",
        "task_brush_teeth": "Cepillarse los Dientes",
        "task_snack_time": "Hora de la Merienda",
        "task_play_time": "Hora de Jugar",
        "task_park_trip": "Paseo por el Parque",
        "task_lunch": "Almuerzo",
        "task_go_home": "Ir a Casa",
        "tap_to_speak": "Toca para Hablar",
        "nav_home": "Inicio",
        "nav_plan": "Plan",
        "nav_rewards": "Premios",
        "nav_profile": "Perfil"
    },
    "fr": {
        "morning_route": "Routine Matinale",
        "hi_leo": "Salut, Leo ! 👋",
        "todays_adventure": "L'Aventure du Jour",
        "tasks_count": "8 Tâches",
        "task_circle_time": "Temps d'Échange",
        "task_wash_hands": "Se Laver les Mains",
        "task_brush_teeth": "Se Brosser les Dents",
        "task_snack_time": "Heure du Goûter",
        "task_play_time": "Temps de Jeu",
        "task_park_trip": "Sortie au Parc",
        "task_lunch": "Déjeuner",
        "task_go_home": "Rentrer à la Maison",
        "tap_to_speak": "Appuie pour Parler",
        "nav_home": "Accueil",
        "nav_plan": "Plan",
        "nav_rewards": "Récompenses",
        "nav_profile": "Profil"
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const langButtons = document.querySelectorAll('.lang-btn');
    const elementsToTranslate = document.querySelectorAll('[data-i18n]');

    // Function to update texts based on language
    function setLanguage(lang) {
        if (!translations[lang]) return;

        const currentTranslations = translations[lang];

        elementsToTranslate.forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (currentTranslations[key]) {
                element.textContent = currentTranslations[key];
            }
        });
    }

    // Add click events to language buttons
    let currentSelectedLang = 'en'; // Default language
    langButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            langButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            // Update language
            currentSelectedLang = button.getAttribute('data-lang');
            setLanguage(currentSelectedLang);
        });
    });

    // --- Voice Translation Logic ---
    const micButton = document.querySelector('.mic-button');
    const micLabelText = document.querySelector('.mic-label p');

    // Check if Web Speech API is supported
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;

    if (!SpeechRecognition || !synth) {
        console.warn("Web Speech API is not supported in this browser.");
        micButton.style.opacity = '0.5';
        micButton.style.cursor = 'not-allowed';
        return; // Exit if not supported
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    // Use a free translation API (MyMemory) for demonstration purposes
    // Note: Free APIs have rate limits. A production app would need a paid service.
    async function translateText(text, sourceLang, targetLang) {
        try {
            const response = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=${sourceLang}|${targetLang}`);
            const data = await response.json();
            return data.responseData.translatedText;
        } catch (error) {
            console.error("Translation error:", error);
            return "Erro na tradução / Translation error";
        }
    }

    // Function to speak the translated text
    function speakText(text, lang) {
        if (synth.speaking) {
            console.error('speechSynthesis.speaking');
            return;
        }

        let utterance = new SpeechSynthesisUtterance(text);

        // Map data-lang to BCP 47 language tags for SpeechSynthesis
        const langMap = {
            'en': 'en-US',
            'pt': 'pt-BR',
            'es': 'es-ES',
            'fr': 'fr-FR'
        };

        utterance.lang = langMap[lang] || 'en-US';

        // Optional: find a specific voice if needed, otherwise uses default for the lang
        const voices = synth.getVoices();
        const specificVoice = voices.find(voice => voice.lang.includes(utterance.lang));
        if (specificVoice) {
            utterance.voice = specificVoice;
        }

        synth.speak(utterance);
    }

    let isRecording = false;

    micButton.addEventListener('mousedown', (e) => {
        e.preventDefault(); // Prevent text selection
        if (isRecording) return;

        isRecording = true;
        micButton.style.transform = 'scale(0.9)';
        micLabelText.textContent = currentSelectedLang === 'pt' ? 'Ouvindo...' : 'Listening...';

        // By default, assume the user is speaking Portuguese
        // If the selected language is already Portuguese, we could assume they are speaking pt to pt (no-op)
        // or we allow them to speak the other language to translate to PT.
        // Let's set recognition language to Portuguese for now to translate PT -> Selected Lang.
        recognition.lang = 'pt-BR';
        recognition.start();
    });

    const stopRecording = () => {
        if (!isRecording) return;
        isRecording = false;
        micButton.style.transform = 'none';
        micLabelText.textContent = translations[currentSelectedLang]['tap_to_speak'] || 'Tap to Speak';
        recognition.stop();
    };

    micButton.addEventListener('mouseup', stopRecording);
    micButton.addEventListener('mouseleave', stopRecording);

    // Support for touch devices
    micButton.addEventListener('touchstart', (e) => {
        e.preventDefault();
        micButton.dispatchEvent(new Event('mousedown'));
    });
    micButton.addEventListener('touchend', (e) => {
        e.preventDefault();
        stopRecording();
    });

    recognition.onresult = async (event) => {
        const transcript = event.results[0][0].transcript;
        console.log("Original (PT):", transcript);
        micLabelText.textContent = 'Traduzindo...';

        // Translate from Portuguese to the currently selected language
        // If the selected language IS Portuguese, translate from English to Portuguese as a fallback
        let sourceLang = 'pt';
        let targetLang = currentSelectedLang;
        let speakLang = currentSelectedLang;

        if (currentSelectedLang === 'pt') {
            sourceLang = 'en'; // Assuming if PT is selected, they might speak EN to translate to PT
            targetLang = 'pt';
            speakLang = 'pt';
        }

        const translatedText = await translateText(transcript, sourceLang, targetLang);
        console.log(`Translated (${targetLang}):`, translatedText);

        micLabelText.textContent = translations[currentSelectedLang]['tap_to_speak'] || 'Tap to Speak';
        speakText(translatedText, speakLang);
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        stopRecording();
    };
});

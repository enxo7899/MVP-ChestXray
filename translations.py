"""
Medical Pathology Translations - English to Albanian

Proper medical terminology for chest X-ray pathologies.
Based on standard Albanian medical literature and Latin medical terms.
"""

# Pathology translations: English -> Albanian (Medical Terms)
PATHOLOGY_TRANSLATIONS = {
    # English Name: (Albanian Name, Latin Term)
    "Atelectasis": ("Atelektazë", "Atelectasis"),
    "Cardiomegaly": ("Kardiomegali", "Cardiomegalia"),
    "Consolidation": ("Konsolidim Pulmonar", "Consolidatio"),
    "Edema": ("Edemë Pulmonare", "Oedema Pulmonale"),
    "Effusion": ("Efuzion Pleural", "Effusio Pleuralis"),
    "Emphysema": ("Emfizemë", "Emphysema"),
    "Enlarged Cardiomediastinum": ("Kardiomediastinum i Zgjeruar", "Cardiomediastinum Dilatatum"),
    "Fibrosis": ("Fibrozë Pulmonare", "Fibrosis Pulmonalis"),
    "Fracture": ("Frakturë", "Fractura"),
    "Hernia": ("Hernie", "Hernia"),
    "Infiltration": ("Infiltrim Pulmonar", "Infiltratio Pulmonalis"),
    "Lung Lesion": ("Lezion Pulmonar", "Laesio Pulmonalis"),
    "Lung Opacity": ("Opacitet Pulmonar", "Opacitas Pulmonalis"),
    "Mass": ("Masë Pulmonare", "Massa Pulmonalis"),
    "Nodule": ("Nodul Pulmonar", "Nodulus Pulmonalis"),
    "Pleural Thickening": ("Trashje Pleurale", "Incrassatio Pleuralis"),
    "Pneumonia": ("Pneumoni", "Pneumonia"),
    "Pneumothorax": ("Pneumotoraks", "Pneumothorax"),
    
    # Additional possible pathologies
    "No Finding": ("Pa Gjetje Patologjike", "Sine Morbo"),
    "Support Devices": ("Pajisje Mbështetëse", "Apparatus Sustentans"),
}


def translate_pathology(english_name: str, include_latin: bool = False) -> str:
    """
    Translate pathology name from English to Albanian.
    
    Args:
        english_name: English pathology name
        include_latin: If True, includes Latin term in parentheses
        
    Returns:
        Albanian translation (with optional Latin term)
        
    Example:
        >>> translate_pathology("Pneumonia")
        "Pneumoni"
        >>> translate_pathology("Pneumonia", include_latin=True)
        "Pneumoni (Pneumonia)"
    """
    if english_name in PATHOLOGY_TRANSLATIONS:
        albanian, latin = PATHOLOGY_TRANSLATIONS[english_name]
        if include_latin:
            return f"{albanian} ({latin})"
        return albanian
    
    # If translation not found, return original
    return english_name


def get_all_translations() -> dict:
    """
    Get all pathology translations as a dictionary.
    
    Returns:
        Dictionary mapping English names to Albanian names
    """
    return {
        english: albanian 
        for english, (albanian, _) in PATHOLOGY_TRANSLATIONS.items()
    }


def get_translation_with_latin(english_name: str) -> tuple:
    """
    Get both Albanian and Latin translations.
    
    Args:
        english_name: English pathology name
        
    Returns:
        Tuple of (albanian_name, latin_name)
        
    Example:
        >>> get_translation_with_latin("Pneumonia")
        ("Pneumoni", "Pneumonia")
    """
    if english_name in PATHOLOGY_TRANSLATIONS:
        return PATHOLOGY_TRANSLATIONS[english_name]
    return (english_name, english_name)

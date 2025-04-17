import streamlit as st
import chardet

# Book code mapping
book_codes = {
    "1": "Genesis", "2": "Exodus", "3": "Leviticus", "4": "Numbers", "5": "Deuteronomy",
    "6": "Joshua", "7": "Judges", "8": "Ruth", "9": "1 Samuel", "10": "2 Samuel",
    "11": "1 Kings", "12": "2 Kings", "13": "1 Chronicles", "14": "2 Chronicles",
    "15": "Ezra", "16": "Nehemiah", "17": "Esther", "18": "Job", "19": "Psalms",
    "20": "Proverbs", "21": "Ecclesiastes", "22": "Song of Solomon", "23": "Isaiah",
    "24": "Jeremiah", "25": "Lamentations", "26": "Ezekiel", "27": "Daniel", "28": "Hosea",
    "29": "Joel", "30": "Amos", "31": "Obadiah", "32": "Jonah", "33": "Micah", "34": "Nahum",
    "35": "Habakkuk", "36": "Zephaniah", "37": "Haggai", "38": "Zechariah", "39": "Malachi",
    "40": "Matthew", "41": "Mark", "42": "Luke", "43": "John", "44": "Acts", "45": "Romans",
    "46": "1 Corinthians", "47": "2 Corinthians", "48": "Galatians", "49": "Ephesians",
    "50": "Philippians", "51": "Colossians", "52": "1 Thessalonians", "53": "2 Thessalonians",
    "54": "1 Timothy", "55": "2 Timothy", "56": "Titus", "57": "Philemon", "58": "Hebrews",
    "59": "James", "60": "1 Peter", "61": "2 Peter", "62": "1 John", "63": "2 John", "64": "3 John",
    "65": "Jude", "66": "Revelation",
}

def process_file(file):
    raw = file.read()
    encoding = chardet.detect(raw)['encoding'] or 'utf-8'

    try:
        content = raw.decode(encoding)
    except UnicodeDecodeError:
        st.error(f"Could not decode the file with detected encoding: {encoding}")
        return []

    lines = content.splitlines()
    output_lines = []

    for line in lines:
        if line.startswith("Bm"):
            try:
                _, value = line.split("=", 1)
                parts = value.split(":")
                if len(parts) == 4:
                    _, book_number, chapter, verse = parts
                    book_name = book_codes.get(book_number, f"Unknown Book ({book_number})")
                    output_lines.append(f"{book_name}, {chapter}:{verse}")
                else:
                    output_lines.append(f"Invalid Format: {line.strip()}")
            except Exception:
                output_lines.append(f"Invalid Format: {line.strip()}")
        else:
            output_lines.append(f"Invalid Format: {line.strip()}")

    return output_lines

# --- Streamlit UI ---
st.title("📖 Bible Verse Reference Converter")
st.write("Upload a file formatted like `Bm=KJV:1:1:1`, and get human-readable Bible references.")

# ✅ Allow both .txt and .prg files
uploaded_file = st.file_uploader("Upload your file (.txt or .prg)", type=["txt", "prg"])

if uploaded_file:
    result = process_file(uploaded_file)

    if result:
        output_text = "\n".join(result)
        st.download_button("Download Converted File", data=output_text, file_name="converted_output.txt")
        st.text_area("Converted Output", output_text, height=300)

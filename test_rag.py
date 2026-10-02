
from app.services.qa_service import answer_question


pdf_path = "data/documents/Unit 4_.pdf"

question = "What are the global logistics trends?"

answer, sources = answer_question(pdf_path, question)

print("\nANSWER:")
print(answer)

print("\nSOURCES:")

for i, source in enumerate(sources, 1):
    print(f"\n--- Source {i} ---")
    print(source)
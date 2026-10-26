import fitz, sys
sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open(r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf')

for p in range(180, 190):
    page = doc[p]
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if 'lines' in b:
            for line in b['lines']:
                line_text = ''.join(span['text'] for span in line['spans']).strip()
                for target in [
                    'Отшельнический устав',
                    'Анахоретские монастыри древнего христианского Египта',
                    'Нитрия', 'Келлии', 'Скит',
                    'Другие анахоретские монастыри Египта',
                    'Прп. Пахомий и его монастыри'
                ]:
                    if target in line_text:
                        span = line['spans'][0]
                        print(f'Page {p+1}: Heading "{line_text}", size={span["size"]:.1f}, flags={span["flags"]}, font={span["font"]}')

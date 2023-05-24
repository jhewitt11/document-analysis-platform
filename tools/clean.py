import re

def chunkify(text, LIMIT, OVERLAP, stats = False) :
    '''
    Split text string into chunks no larger than LIMIT unless an entire sentence is longer. OVERLAP 
    '''
    OVERLAP = int(OVERLAP)
    assert(OVERLAP > 0 )

    sentences = text.split('. ')
    new_sents = [x + '. ' for x in sentences]

    chunks = []
    chunk_lengths = []
    current_chunk = ''

    # current issue : '' starting chunk when theres a long initial sentence

    for sent in new_sents:
        if len(current_chunk) + len(sent) > LIMIT:
            if current_chunk != '' :
                chunks.append(current_chunk)
                chunk_lengths.append(len(current_chunk))
            current_chunk = current_chunk[-OVERLAP:] + sent

        else :
            current_chunk += sent
    chunks.append(current_chunk)
    chunk_lengths.append(len(current_chunk))

    if stats:
        #print(chunk_lengths)
        chunk_lengths.sort()
        low_quart = int(len(chunk_lengths)/4)
        upper_quart = low_quart * 3
        print(
            f'Number of chunks : {len(chunk_lengths)}'
            f'\nMin : {chunk_lengths[0]}'
            f'\n25% : {chunk_lengths[low_quart]}'
            f'\n75% : {chunk_lengths[upper_quart]}'
            f'\nMax : {chunk_lengths[-1]}'
        )

    return chunks

def clean_text(text) :
    '''
    Simplify text. Remove non utf-8 characters and consecutive whitespaces.
    '''

    text = bytes(text, 'utf-8').decode('utf-8','ignore')
    text = re.sub(r'\s+', ' ', text)

    return text

def clean_dictionary(query_dict):
    '''
    Query will be excluded from cleaning in this process.

    Only fetched results will be cleaned.
    '''

  #  cleaned_dict = query_dict.copy()
    results = query_dict['results']

    for result in results:

        result['title'] = clean_text( result['title'] )
        result['link'] = clean_text( result['link'] )
        result['text'] = clean_text( result['text'])

    return query_dict
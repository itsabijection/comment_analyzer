import numpy as np
import gensim

#sparingly adapted from quadrismigestus
#https://gist.github.com/quadrismegistus/09a93e219a6ffc4f216fb85235535faf

def procrustes(base_embed, other_embed):
	base_embed.init_sims()
	other_embed.init_sims()

	#vectors
	in_base_embed, in_other_embed = intersect(base_embed, other_embed)
	base_vecs = in_base_embed.wv.vectors_norm
	other_vecs = in_other_embed.wv.vectors_norm

	#dot product
	m = other_vecs.T.dot(base_vecs) 
	# SVD
	u, _, v = np.linalg.svd(m)
	#multiply the embedding matrix (vectors_norm) by u.dot(v)
	other_embed.wv.vectors_norm = other_embed.wv.vectors = (other_embed.wv.vectors_norm).dot(u.dot(v))
	return other_embed
	
def intersect(m1,m2, words=None):

	# Get the vocab for each model
	vocab_m1 = set(m1.wv.vocab.keys())
	vocab_m2 = set(m2.wv.vocab.keys())

	# Find the common vocabulary
	common_vocab = vocab_m1&vocab_m2
	if words: 
		common_vocab&=set(words)

	#if symmetric subtraction is nothing then vocabs are the same
	if not vocab_m1-common_vocab and not vocab_m2-common_vocab:
		return (m1,m2)

	# Otherwise sort by frequency (summed for both)
	common_vocab = list(common_vocab)
	common_vocab.sort(key=lambda w: m1.wv.vocab[w].count + m2.wv.vocab[w].count,reverse=True)

    #for each model
	for m in [m1,m2]:
		# Replace old vectors_norm array with with common vocab vectors
		indices = [m.wv.vocab[w].index for w in common_vocab]
		old_arr = m.wv.vectors_norm
		new_arr = np.array([old_arr[index] for index in indices])
		m.wv.vectors_norm = m.vectors = new_arr
		# Replace old vocab dictionary with new one (with common vocab)
		# and old index2word with new one
		m.index2word = common_vocab
		old_vocab = m.wv.vocab
		new_vocab = {}
		for new_index,word in enumerate(common_vocab):
			old_vocab_obj=old_vocab[word]
			new_vocab[word] = gensim.models.word2vec.Vocab(index=new_index, count=old_vocab_obj.count)
		m.wv.vocab = new_vocab

	return (m1,m2)
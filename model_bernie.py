import numpy as np
import tensorflow as tf
#from model_embedding import RGCN_embedding
from data_loader import build_data_loader
from rgcn import RGCN,DistMult,RGCN_Input,RGCN_Hidden

adj_years=[]
feature_years=[]
train_years=[]
val_years=[]
alignment_indices=[]
past_paper_ids=None

train_prop=.1
val_prop=.05
negative_rate=10


for year in range(2005,2010):
    print(year)
    data_loader=build_data_loader(year,'/home/songjiang/bernie/projects/field_emergence/data/processed/',True)
    train_years.append((tf.convert_to_tensor(data_loader['train_samples'],dtype='int32'),tf.convert_to_tensor(data_loader['train_labels'],dtype='float32')))
    val_years.append((tf.convert_to_tensor(data_loader['train_samples'],dtype='int32'),tf.convert_to_tensor(data_loader['train_labels'],dtype='float32')))
    feature_years.append(tf.convert_to_tensor(data_loader['node_features'],dtype='float32'))
    
    num_nodes=data_loader['node_ids'].shape[0]
    adj_matrices=[]
    for i in range(data_loader['num_rels']):
        edges_of_type=data_loader['all_edges'][data_loader['all_edges'][:,1]==i]
        mat=tf.dtypes.cast(
            tf.sparse.SparseTensor(indices=edges_of_type[:,(0,2)],
                                   values=edges_of_type[:,3],
                                   dense_shape=[num_nodes,num_nodes]),
            'float32')
        adj_matrices.append(mat)
    self_loop_indices=np.vstack((np.arange(num_nodes),np.arange(num_nodes))).transpose()
    self_loop=tf.dtypes.cast(
        tf.sparse.SparseTensor(indices=self_loop_indices,
                                   values=np.ones(num_nodes),
                                   dense_shape=[num_nodes,num_nodes]),
        'float32')
    adj_matrices.append(self_loop)
    adj_years.append(adj_matrices)
    
    paper_ids=data_loader['node_ids'][data_loader['node_features'][:,0]==1]
    if type(past_paper_ids) is np.ndarray:
        _,past_indices,curr_indices=np.intersect1d(past_paper_ids,paper_ids,return_indices =True)
        alignment_indices.append((past_indices,curr_indices))
    past_paper_ids=paper_ids
        

class RGCN_Autoencoder(tf.keras.Model):
    def __init__(self,
                 adj_list,
                 node_features,
                 relations,
                 graph_index,
                 intermediate_dim=64,
                 latent_dim=128,
                 name='rgcn_autencoder',
                 **kwargs):
        super(RGCN_Autoencoder, self).__init__(name=name, **kwargs)
        self.adj_list=adj_list
        self.node_features=node_features
        
        self.encoder_input=RGCN_Input(out_dim=intermediate_dim,
                                      graph_index=graph_index,
                                      relations=relations,
                                      activation='relu')
        self.encoder_hidden=RGCN_Hidden(out_dim=latent_dim,
                                        graph_index=graph_index,
                                       relations=relations)
        self.decoder=DistMult(graph_index=graph_index)
        

    def call(self,inputs):
        H1=self.encoder_input([self.adj_list,self.node_features])
        H2=self.encoder_hidden([self.adj_list, H1])
        score=self.decoder([inputs ,H2])
        
        return score
    

autoencoder=RGCN_Autoencoder(adj_list=adj_years[0],
                            node_features=feature_years[0],
                            relations= ['PcP','PbA','PiV','PuK','PbP','AwP','VpP','KpP','self'],
                            graph_index=0,
                            intermediate_dim=64,
                            latent_dim=128)

optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
bce_loss_fn = tf.keras.losses.binary_crossentropy
loss_metric = tf.keras.metrics.Mean()

with tf.GradientTape() as tape:
    preds=autoencoder(train_years[0][0])
    loss=bce_loss_fn(preds,train_years[0][1],from_logits=True)

grads = tape.gradient(loss, autoencoder.trainable_weights)
optimizer.apply_gradients(zip(grads, autoencoder.trainable_weights))

loss_metric(loss)




H1=RGCN_Input(out_dim=64,graph_index=0,activation='relu')([adj_years[0],feature_years[0]])
H2=RGCN_Hidden(out_dim=128,graph_index=0)([adj_years[0], H1])
score=DistMult(graph_index=0)([train_years[0][0],H2])
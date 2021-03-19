from agcn.configs.common_configs import *

class ConfigTrainJointLoader(ConfigTrainBoneLoader):
  
    work_dir="./work_dir/ntu/xsub/agcn_joint"
    model_saved_name="./runs/ntu_cs_agcn_joint"
    
    # feeder
    feeder="feeders.feeder.Feeder"
    train_feeder_args= TrainFeederArgs(
                                        data_path="/data/ntu/xsub/train_data_joint.npy",
                                        label_path="/data/ntu/xsub/train_label.pkl",
                                        debug=False,
                                        random_choose=False,
                                        random_shift=False,
                                        random_move=False,
                                        window_size=-1, 
                                        normalization=False
                                    )
    test_feeder_args=TestFeederArgs(
                                    data_path="/data/ntu/xsub/val_data_joint.npy",
                                    label_path="/data/ntu/xsub/val_label.pkl"
                                    )
    
    # model
    model="model.agcn.UnitAGCN"
    model_args= ModelArgs(
                            num_class= 60,
                            num_point= 25,
                            num_person= 2,
                            graph= "graph.ntu_rgb_d.Graph",
                            graph_args=GraphArgs(labeling_mode= 'spatial')
                        )
   
    #optim
    weight_decay=0.0001
    base_lr=0.1
    step=[30, 40]

    # training
    phase="train"
    device=[0]
    batch_size=6
    test_batch_size=64
    num_epoch=50
    nesterov=True
    
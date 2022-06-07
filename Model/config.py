import torch
import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--seed", default=42, type=int, help="seed"
    )
    parser.add_argument(
        '--device', default='cuda' if torch.cuda.is_available() else 'cpu', type=str, help="cpu or gpu"
    )
    parser.add_argument(
        "--img_dir", default="/opt/ml/musinsa_dataset/images", type=str, help="data directory"
    )
    parser.add_argument(
        "--data_dir", default="/opt/ml/musinsa_dataset/data", type=str, help="data directory"
    )
    parser.add_argument(
        "--file_name", default="articles.csv", type=str, help="train file name"
    )
    parser.add_argument(
        "--asset_dir", default="/opt/ml/musinsa_dataset/asset/", type=str, help="data directory"
    )
    parser.add_argument(
        "--asset_file", default="fe_data.csv", type=str, help="extracted data file name"
    )
    parser.add_argument(
        "--model_dir", default="/opt/ml/musinsa_dataset/models/", type=str, help="model directory"
    )
    parser.add_argument(
        "--model_name", default="test_model.pt", type=str, help="model file name"
    )
    parser.add_argument(
        "--test_dir", default="/opt/ml/musinsa_dataset/test/", type=str, help="test file directory"
    )
    parser.add_argument(
        "--test_file_name", default="test_img.jpg", type=str, help="test file name"
    )
    parser.add_argument(
        "--output_dir", default="/opt/ml/musinsa_dataset/output/", type=str, help="output directory"
    )
    parser.add_argument(
        "--output_file_name", default="output.jpg", type=str, help="output file name"
    )

    # preprocess
    parser.add_argument(
        "--ratio", default=0.8, type=float, help="the proportion of the train dataset"
    )
    parser.add_argument(
        "--limit_num", default=1000, type=int, help="number of images per class"
    )
    parser.add_argument(
        "--product2id", nargs="+", default={}, type=dict, help="dictionary that matches product names with ids"
    )    
    parser.add_argument(
        "--id2product", nargs="+", default={0: "Top", 
                                            1: "Top",
                                            2: "Top",
                                            3: "Outer",
                                            4: "Outer",
                                            5: "Outer",
                                            6: "Pants",
                                            7: "Pants",
                                            8: "Pants",
                                            9: "Bag",
                                            10: "Bag",
                                            11: "Bag",
                                            12: "Shoes",
                                            13: "Shoes", 
                                            14: "Shoes",
                                            15: "Headwear",
                                            16: "Headwear",
                                            17: "Headwear",
                                            18: "Sneakers",
                                            19: "OnePiece",
                                            20: "OnePiece",
                                            21: "OnePiece",
                                            22: "Skirt",
                                            23: "Skirt",
                                            24: "Skirt"}, type=dict, help="dictionary that matches ids with product names"
    )

    # model
    # efficientnet-b0인 경우 1280*7*7=62720
    # resnet18, resnet34인 경우 512
    # resnet50인 경우 2048
    parser.add_argument(
        "--pre_model", default='resnet34', type=str, help="Limit the number of data augmentation per user"
    )
    parser.add_argument(
        "--model", default="mlp", type=str, help="model type"
    )
    parser.add_argument(
        "--hidden_dim", default=512, type=int, help="hidden dimension size"
    ) 
    parser.add_argument(
        "--output_dim", default=13, type=int, help="output dimension size"
    ) 
    parser.add_argument(
        "--drop_out", default=0.3, type=float, help="drop out rate"
    )

    # train
    parser.add_argument("--n_epochs", default=30, type=int, help="number of epochs")
    parser.add_argument("--batch_size", default=32, type=int, help="batch size")
    parser.add_argument("--optimizer", default="adam", type=str, help="optimizer type")
    parser.add_argument("--w_decay", default=1e-5, type=float, help="weight decay")
    parser.add_argument("--lr", default=0.0005, type=float, help="learning rate")
    parser.add_argument("--clip_grad", default=10, type=int, help="clip grad")
    parser.add_argument("--patience", default=10, type=int, help="for early stopping")
    parser.add_argument(
        "--log_steps", default=50, type=int, help="print log per n steps"
    )
    parser.add_argument(
        "--scheduler", default="plateau", type=str, help="scheduler type"
    )
   
    # inference
    parser.add_argument("--k", default=5, type=int, help="number of output images")
    parser.add_argument("--similarity", default="cos", type=str, help="similarity type")
    

    args = parser.parse_args()

    return args

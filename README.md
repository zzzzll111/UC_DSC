# UC_DSC-code-
This repository is the code part of our paper `UC_DSC`. 

`privatechain_macos_folder` contains various information related to private chains on macOS, such as the genesis block, accounts, keys, and more.

`privatechain_windows_folder` holds similar information for private chains on Windows.

`uc_DSC_code_folder` serves as the core framework of this project.

Within this framework, `dataset_process` is responsible for processing datasets to ensure they can be effectively encrypted and utilized.

`file_blocks` mainly handles the splitting and merging of files by length, allowing them to better fit various storage environments with length restrictions.

`OPE`  primarily stores the source code implementation of the order-preserving encryption used in this project.

`zkSNARK` contains the source code for the zero-knowledge proofs utilized in this work.

`bin_file_operate`  includes the necessary source code for processing binary files, mainly responsible for converting strings or non-binary files into binary for subsequent operations.

`myclass.py` contains the class library defined in this project, primarily consisting of two classes: **worker** and **requester** , each equipped with several methods, including **Location_Policy_Verification** .etc, corresponding to the ideal functions discussed in the text.

`get_center.py`, `vet_vec_u_workers.py`, and `vet_vec_v_circule.py` are mainly used to map random geographical locations to grid centers under the specified privacy protection levels, generating the corresponding circles.

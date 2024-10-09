const { Web3 } = require('web3');
const web3 = new Web3('http://localhost:8545'); // 节点端口号

async function measureTxpoolTime() {
    const account = '0xa1f2fa0abe77fc98a4195294c7088b78386805bf'; // 转出的账户
    const recipient = '0x4064182fb50107610a5d61ec2219b28771cd846a'; // 接收者地址
    const value = web3.utils.toWei('1', 'wei'); // 转账金额设置为1wei

    // 记录发送交易的时间
    const startTime = Date.now();

    try {
        // 发送交易
        const txHash = await web3.eth.sendTransaction({
            from: account,
            to: recipient,
            value: value,
            gas: 21000,
            gasPrice: '20000000000' // 20 Gwei
        });

        console.log("Transaction sent, waiting for it to enter txpool...");

        // 监听 txpool 中交易的数量变化
        let txpoolCount = await web3.eth.getTransactionPool();
        let initialCount = txpoolCount.pending[account] ? Object.keys(txpoolCount.pending[account]).length : 0;

        const checkInterval = setInterval(async () => {
            txpoolCount = await web3.eth.getTransactionPool();
            let currentCount = txpoolCount.pending[account] ? Object.keys(txpoolCount.pending[account]).length : 0;
            if (currentCount > initialCount) {
                const endTime = Date.now();
                console.log(`Transaction entered txpool after ${(endTime - startTime)} milliseconds`);
                clearInterval(checkInterval);
            }
        }, 1000);

    } catch (error) {
        console.error('An error occurred:', error);
    }
}

measureTxpoolTime();






//node measureTxpoolTime.js

const { spawn } = require('child_process');

const pythonProcess = spawn('python', ['../../motor/main.py']);

pythonProcess.stdout.on('data', (data) => {
    console.log(`Python diz: ${data}`);
});

pythonProcess.stderr.on('data', (data) => {
    console.error(`Erro do Python: ${data}`);
});

pythonProcess.on('close', (code) => {
    console.log(`Python finalizou com código ${code}`);
});
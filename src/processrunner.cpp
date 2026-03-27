#include "processrunner.h"
#include <QDebug>

ProcessRunner::ProcessRunner(QObject *parent)
    : QObject(parent)
{
    process = new QProcess(this);
    
    connect(process, &QProcess::readyReadStandardOutput,
            this, &ProcessRunner::handleReadyReadStandardOutput);
    connect(process, &QProcess::readyReadStandardError,
            this, &ProcessRunner::handleReadyReadStandardError);
    connect(process, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished),
            this, &ProcessRunner::handleProcessFinished);
}

ProcessRunner::~ProcessRunner()
{
    if (process->state() != QProcess::NotRunning) {
        process->kill();
        process->waitForFinished();
    }
}

void ProcessRunner::runCommand(const QString &command, const QStringList &arguments, const QString &workingDir)
{
    if (process->state() != QProcess::NotRunning) {
        emit errorReceived("ERROR: Process already running");
        return;
    }
    
    if (!workingDir.isEmpty()) {
        process->setWorkingDirectory(workingDir);
    }
    
    // Merge stderr and stdout for better output capture
    process->setProcessChannelMode(QProcess::MergedChannels);
    
    emit outputReceived("Starting command: " + command + " " + arguments.join(" "));
    emit processStarted();
    process->start(command, arguments);
    
    if (!process->waitForStarted(5000)) {
        QString errorMsg = "ERROR: Failed to start process: " + command + "\n";
        errorMsg += "Error: " + process->errorString();
        emit errorReceived(errorMsg);
    } else {
        emit outputReceived("Process started successfully, waiting for output...");
    }
}

void ProcessRunner::stopProcess()
{
    if (process->state() != QProcess::NotRunning) {
        process->terminate();
        
        // Give it a chance to terminate gracefully
        if (!process->waitForFinished(3000)) {
            process->kill();
        }
    }
}

bool ProcessRunner::isRunning() const
{
    return process->state() != QProcess::NotRunning;
}

void ProcessRunner::handleReadyReadStandardOutput()
{
    QString output = QString::fromLocal8Bit(process->readAllStandardOutput());
    emit outputReceived(output);
}

void ProcessRunner::handleReadyReadStandardError()
{
    QString error = QString::fromLocal8Bit(process->readAllStandardError());
    emit errorReceived(error);
}

void ProcessRunner::handleProcessFinished(int exitCode, QProcess::ExitStatus exitStatus)
{
    Q_UNUSED(exitStatus);
    emit processFinished(exitCode);
}

#ifndef PROCESSRUNNER_H
#define PROCESSRUNNER_H

#include <QObject>
#include <QProcess>
#include <QString>

class ProcessRunner : public QObject
{
    Q_OBJECT

public:
    explicit ProcessRunner(QObject *parent = nullptr);
    ~ProcessRunner();
    
    void runCommand(const QString &command, const QStringList &arguments, const QString &workingDir);
    void stopProcess();
    bool isRunning() const;

signals:
    void processStarted();
    void processFinished(int exitCode);
    void outputReceived(const QString &output);
    void errorReceived(const QString &error);

private slots:
    void handleReadyReadStandardOutput();
    void handleReadyReadStandardError();
    void handleProcessFinished(int exitCode, QProcess::ExitStatus exitStatus);

private:
    QProcess *process;
};

#endif // PROCESSRUNNER_H

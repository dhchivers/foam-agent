#ifndef CASEMANAGER_H
#define CASEMANAGER_H

#include <QObject>
#include <QString>
#include <QDir>
#include <QMap>
#include "processrunner.h"

class CaseManager : public QObject
{
    Q_OBJECT

public:
    explicit CaseManager(QObject *parent = nullptr);
    ~CaseManager();
    
    // Case operations
    bool createNewCase(const QString &path);
    bool openCase(const QString &path);
    bool saveCase();
    bool closeCase();
    
    // Getters
    QString currentCasePath() const { return m_casePath; }
    QString currentCaseName() const;
    bool hasOpenCase() const { return !m_casePath.isEmpty(); }
    
    // OpenFOAM specific operations
    bool runBlockMesh();
    bool runSolver(const QString &solverName);
    bool runParaFoam();
    bool runCheckMesh();
    QStringList getAvailableSolvers() const;
    QStringList getCaseFiles() const;

signals:
    void caseOpened(const QString &path);
    void caseClosed();
    void statusMessage(const QString &message);
    void logMessage(const QString &message);
    void processStarted(const QString &processName);
    void processFinished(const QString &processName, int exitCode);

public slots:
    void stopCurrentProcess();

private:
    bool createCaseStructure();
    bool createControlDict();
    bool createFvSchemes();
    bool createFvSolution();
    bool validateCaseStructure(const QString &path);
    
    QString m_casePath;
    QMap<QString, QString> m_caseSettings;
    ProcessRunner *m_processRunner;
};

#endif // CASEMANAGER_H

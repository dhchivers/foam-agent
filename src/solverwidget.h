#ifndef SOLVERWIDGET_H
#define SOLVERWIDGET_H

#include <QWidget>
#include <QPushButton>
#include <QTextEdit>
#include <QComboBox>
#include <QGroupBox>
#include <QProgressBar>
#include <QLabel>
#include "casemanager.h"

class SolverWidget : public QWidget
{
    Q_OBJECT

public:
    explicit SolverWidget(CaseManager *manager, QWidget *parent = nullptr);
    ~SolverWidget();

private slots:
    void selectSolver(int index);
    void runSolver();
    void stopSolver();
    void updateProgress();
    void appendLog(const QString &message);

private:
    void setupUI();
    void populateSolvers();
    
    CaseManager *caseManager;
    
    QGroupBox *solverGroup;
    QComboBox *solverCombo;
    QLabel *solverDescription;
    QPushButton *runButton;
    QPushButton *stopButton;
    
    QGroupBox *progressGroup;
    QProgressBar *progressBar;
    QLabel *timeLabel;
    QLabel *iterationLabel;
    
    QTextEdit *solverLogText;
};

#endif // SOLVERWIDGET_H

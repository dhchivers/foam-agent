#include "solverwidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QMessageBox>

SolverWidget::SolverWidget(CaseManager *manager, QWidget *parent)
    : QWidget(parent), caseManager(manager)
{
    setupUI();
    populateSolvers();
}

SolverWidget::~SolverWidget()
{
}

void SolverWidget::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Solver selection
    solverGroup = new QGroupBox("Solver Selection", this);
    QVBoxLayout *solverLayout = new QVBoxLayout();
    
    solverCombo = new QComboBox(this);
    solverLayout->addWidget(new QLabel("Select Solver:"));
    solverLayout->addWidget(solverCombo);
    
    solverDescription = new QLabel(this);
    solverDescription->setWordWrap(true);
    solverDescription->setStyleSheet("QLabel { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }");
    solverLayout->addWidget(solverDescription);
    
    QHBoxLayout *controlLayout = new QHBoxLayout();
    runButton = new QPushButton("Run Solver", this);
    runButton->setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }");
    stopButton = new QPushButton("Stop Solver", this);
    stopButton->setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; padding: 10px; }");
    stopButton->setEnabled(false);
    
    controlLayout->addWidget(runButton);
    controlLayout->addWidget(stopButton);
    solverLayout->addLayout(controlLayout);
    
    solverGroup->setLayout(solverLayout);
    mainLayout->addWidget(solverGroup);
    
    // Progress monitoring
    progressGroup = new QGroupBox("Solver Progress", this);
    QVBoxLayout *progressLayout = new QVBoxLayout();
    
    progressBar = new QProgressBar(this);
    progressBar->setRange(0, 100);
    progressLayout->addWidget(progressBar);
    
    QHBoxLayout *statsLayout = new QHBoxLayout();
    timeLabel = new QLabel("Time: 0.0", this);
    iterationLabel = new QLabel("Iteration: 0", this);
    statsLayout->addWidget(timeLabel);
    statsLayout->addWidget(iterationLabel);
    statsLayout->addStretch();
    progressLayout->addLayout(statsLayout);
    
    progressGroup->setLayout(progressLayout);
    mainLayout->addWidget(progressGroup);
    
    // Solver log
    QLabel *logLabel = new QLabel("Solver Output:", this);
    mainLayout->addWidget(logLabel);
    
    solverLogText = new QTextEdit(this);
    solverLogText->setReadOnly(true);
    solverLogText->setStyleSheet("QTextEdit { font-family: 'Courier New', monospace; }");
    mainLayout->addWidget(solverLogText);
    
    // Connect signals
    connect(solverCombo, QOverload<int>::of(&QComboBox::currentIndexChanged), 
            this, &SolverWidget::selectSolver);
    connect(runButton, &QPushButton::clicked, this, &SolverWidget::runSolver);
    connect(stopButton, &QPushButton::clicked, this, &SolverWidget::stopSolver);
    connect(caseManager, &CaseManager::logMessage, this, &SolverWidget::appendLog);
}

void SolverWidget::populateSolvers()
{
    QStringList solvers = caseManager->getAvailableSolvers();
    
    solverCombo->clear();
    for (const QString &solver : solvers) {
        solverCombo->addItem(solver);
    }
    
    if (!solvers.isEmpty()) {
        selectSolver(0);
    }
}

void SolverWidget::selectSolver(int index)
{
    QString solver = solverCombo->itemText(index);
    
    // Set description based on solver
    if (solver == "icoFoam") {
        solverDescription->setText("Transient solver for incompressible, laminar flow of Newtonian fluids.");
    } else if (solver == "simpleFoam") {
        solverDescription->setText("Steady-state solver for incompressible, turbulent flow.");
    } else if (solver == "pimpleFoam") {
        solverDescription->setText("Transient solver for incompressible flow using PIMPLE algorithm.");
    } else if (solver == "interFoam") {
        solverDescription->setText("Solver for two incompressible, isothermal immiscible fluids using VOF method.");
    } else if (solver == "buoyantSimpleFoam") {
        solverDescription->setText("Steady-state solver for buoyant, turbulent flow of compressible fluids.");
    } else {
        solverDescription->setText("Select a solver to see description.");
    }
}

void SolverWidget::runSolver()
{
    if (!caseManager->hasOpenCase()) {
        QMessageBox::warning(this, "No Case", "Please open or create a case first.");
        return;
    }
    
    QString solver = solverCombo->currentText();
    solverLogText->append("Starting solver: " + solver);
    
    runButton->setEnabled(false);
    stopButton->setEnabled(true);
    
    caseManager->runSolver(solver);
}

void SolverWidget::stopSolver()
{
    solverLogText->append("Stopping solver...");
    caseManager->stopCurrentProcess();
    
    runButton->setEnabled(true);
    stopButton->setEnabled(false);
}

void SolverWidget::updateProgress()
{
    // This will be connected to ProcessRunner signals
    // to update progress bar and labels
}

void SolverWidget::appendLog(const QString &message)
{
    solverLogText->append(message);
    // Auto-scroll to bottom
    QTextCursor cursor = solverLogText->textCursor();
    cursor.movePosition(QTextCursor::End);
    solverLogText->setTextCursor(cursor);
}

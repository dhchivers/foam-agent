#include "mainwindow.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFileDialog>
#include <QMessageBox>
#include <QLabel>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    caseManager = new CaseManager(this);
    
    setupUI();
    createActions();
    createMenus();
    createToolBars();
    createStatusBar();
    
    // Connect case manager signals
    connect(caseManager, &CaseManager::statusMessage, this, &MainWindow::updateStatus);
    connect(caseManager, &CaseManager::logMessage, logWidget, &QTextEdit::append);
    
    updateStatus("Ready");
}

MainWindow::~MainWindow()
{
}

void MainWindow::setupUI()
{
    // Create central widget with tab layout
    QWidget *centralWidget = new QWidget(this);
    QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);
    
    // Create tab widget
    tabWidget = new QTabWidget(this);
    
    // Create widgets for each tab
    meshWidget = new MeshWidget(caseManager, this);
    solverWidget = new SolverWidget(caseManager, this);
    visualizationWidget = new VisualizationWidget(caseManager, this);
    logWidget = new QTextEdit(this);
    logWidget->setReadOnly(true);
    logWidget->setMaximumHeight(150);
    
    // Add tabs
    tabWidget->addTab(meshWidget, "Mesh Generation");
    tabWidget->addTab(solverWidget, "Solver Setup");
    tabWidget->addTab(visualizationWidget, "Visualization");
    
    // Add widgets to layout
    mainLayout->addWidget(tabWidget);
    mainLayout->addWidget(new QLabel("Log:"));
    mainLayout->addWidget(logWidget);
    
    setCentralWidget(centralWidget);
}

void MainWindow::createActions()
{
    newAction = new QAction(tr("&New Case"), this);
    newAction->setShortcut(QKeySequence::New);
    newAction->setStatusTip(tr("Create a new OpenFOAM case"));
    connect(newAction, &QAction::triggered, this, &MainWindow::newCase);
    
    openAction = new QAction(tr("&Open Case"), this);
    openAction->setShortcut(QKeySequence::Open);
    openAction->setStatusTip(tr("Open an existing OpenFOAM case"));
    connect(openAction, &QAction::triggered, this, &MainWindow::openCase);
    
    saveAction = new QAction(tr("&Save Case"), this);
    saveAction->setShortcut(QKeySequence::Save);
    saveAction->setStatusTip(tr("Save the current case"));
    connect(saveAction, &QAction::triggered, this, &MainWindow::saveCase);
    
    closeAction = new QAction(tr("&Close Case"), this);
    closeAction->setShortcut(QKeySequence::Close);
    closeAction->setStatusTip(tr("Close the current case"));
    connect(closeAction, &QAction::triggered, this, &MainWindow::closeCase);
    
    exitAction = new QAction(tr("E&xit"), this);
    exitAction->setShortcut(QKeySequence::Quit);
    exitAction->setStatusTip(tr("Exit the application"));
    connect(exitAction, &QAction::triggered, this, &QWidget::close);
    
    aboutAction = new QAction(tr("&About"), this);
    aboutAction->setStatusTip(tr("Show the application's About box"));
    connect(aboutAction, &QAction::triggered, this, &MainWindow::showAbout);
}

void MainWindow::createMenus()
{
    fileMenu = menuBar()->addMenu(tr("&File"));
    fileMenu->addAction(newAction);
    fileMenu->addAction(openAction);
    fileMenu->addAction(saveAction);
    fileMenu->addAction(closeAction);
    fileMenu->addSeparator();
    fileMenu->addAction(exitAction);
    
    helpMenu = menuBar()->addMenu(tr("&Help"));
    helpMenu->addAction(aboutAction);
}

void MainWindow::createToolBars()
{
    fileToolBar = addToolBar(tr("File"));
    fileToolBar->addAction(newAction);
    fileToolBar->addAction(openAction);
    fileToolBar->addAction(saveAction);
}

void MainWindow::createStatusBar()
{
    statusBar()->showMessage(tr("Ready"));
}

void MainWindow::newCase()
{
    QString dir = QFileDialog::getExistingDirectory(
        this,
        tr("Select Directory for New Case"),
        "/work",
        QFileDialog::ShowDirsOnly | QFileDialog::DontResolveSymlinks
    );
    
    if (!dir.isEmpty()) {
        if (caseManager->createNewCase(dir)) {
            updateStatus(tr("New case created: %1").arg(dir));
        } else {
            QMessageBox::warning(this, tr("Error"), tr("Failed to create new case"));
        }
    }
}

void MainWindow::openCase()
{
    QString dir = QFileDialog::getExistingDirectory(
        this,
        tr("Select OpenFOAM Case Directory"),
        "/work",
        QFileDialog::ShowDirsOnly | QFileDialog::DontResolveSymlinks
    );
    
    if (!dir.isEmpty()) {
        if (caseManager->openCase(dir)) {
            updateStatus(tr("Opened case: %1").arg(dir));
        } else {
            QMessageBox::warning(this, tr("Error"), tr("Failed to open case"));
        }
    }
}

void MainWindow::saveCase()
{
    if (caseManager->saveCase()) {
        updateStatus(tr("Case saved successfully"));
    } else {
        QMessageBox::warning(this, tr("Error"), tr("Failed to save case"));
    }
}

void MainWindow::closeCase()
{
    if (caseManager->closeCase()) {
        updateStatus(tr("Case closed"));
    }
}

void MainWindow::showAbout()
{
    QMessageBox::about(this, tr("About FoamAgent"),
        tr("<h2>FoamAgent 1.0</h2>"
           "<p>A Qt6 application for managing OpenFOAM cases with "
           "web-based visualization and control.</p>"
           "<p>Features:</p>"
           "<ul>"
           "<li>Mesh generation and validation</li>"
           "<li>Solver configuration and execution</li>"
           "<li>Real-time visualization</li>"
           "<li>Web-based access</li>"
           "</ul>"));
}

void MainWindow::updateStatus(const QString &message)
{
    statusBar()->showMessage(message, 5000);
}

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTabWidget>
#include <QTextEdit>
#include <QStatusBar>
#include <QMenuBar>
#include <QToolBar>
#include <QAction>
#include "casemanager.h"
#include "meshwidget.h"
#include "solverwidget.h"
#include "visualizationwidget.h"

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void newCase();
    void openCase();
    void saveCase();
    void closeCase();
    void showAbout();
    void updateStatus(const QString &message);

private:
    void createActions();
    void createMenus();
    void createToolBars();
    void createStatusBar();
    void setupUI();

    // Core components
    CaseManager *caseManager;
    
    // UI Components
    QTabWidget *tabWidget;
    MeshWidget *meshWidget;
    SolverWidget *solverWidget;
    VisualizationWidget *visualizationWidget;
    QTextEdit *logWidget;
    
    // Actions
    QAction *newAction;
    QAction *openAction;
    QAction *saveAction;
    QAction *closeAction;
    QAction *exitAction;
    QAction *aboutAction;
    
    // Menus
    QMenu *fileMenu;
    QMenu *helpMenu;
    
    // Toolbars
    QToolBar *fileToolBar;
};

#endif // MAINWINDOW_H

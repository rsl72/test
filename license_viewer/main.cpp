#include <afxwin.h>
#include <QtWidgets/QApplication>
#include "LicenseViewer.h"

class LicenseApp : public CWinApp {
public:
    BOOL InitInstance() override {
        CWinApp::InitInstance();
        int argc = 0;
        char **argv = nullptr;
        QApplication app(argc, argv);
        LicenseViewer viewer("license_example.md");
        viewer.resize(800, 600);
        viewer.show();
        app.exec();
        return FALSE;
    }
};

LicenseApp theApp;

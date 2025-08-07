#pragma once

#include <QWidget>
#include <QList>
#include <QString>

class QVBoxLayout;

class LicenseViewer : public QWidget {
    Q_OBJECT
public:
    explicit LicenseViewer(const QString &licenseFile, QWidget *parent = nullptr);

private:
    struct Node {
        QString title;
        QString content;
        QList<Node> children;
    };

    QList<Node> parseFile(const QString &path);
    void addNode(const Node &node, QVBoxLayout *layout, int indent = 0);
};

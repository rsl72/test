#include "LicenseViewer.h"

#include <QFile>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QTextEdit>
#include <QVBoxLayout>
#include <QTextStream>
#include <QRegularExpression>

LicenseViewer::LicenseViewer(const QString &licenseFile, QWidget *parent)
    : QWidget(parent) {
    QVBoxLayout *layout = new QVBoxLayout(this);
    const auto nodes = parseFile(licenseFile);
    for (const auto &n : nodes) {
        addNode(n, layout);
    }
    layout->addStretch();
}

QList<LicenseViewer::Node> LicenseViewer::parseFile(const QString &path) {
    QFile file(path);
    QList<Node> roots;
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return roots;
    }
    QTextStream in(&file);
    QList<Node*> stack;
    while (!in.atEnd()) {
        QString line = in.readLine();
        QRegularExpression heading("^(#+)\\s+(.*)");
        auto match = heading.match(line);
        if (match.hasMatch()) {
            int level = match.captured(1).length();
            Node node;
            node.title = match.captured(2);
            if (level == 1) {
                roots.append(node);
                stack.clear();
                stack.append(&roots.last());
            } else {
                while (stack.size() >= level) {
                    stack.removeLast();
                }
                stack.last()->children.append(node);
                stack.append(&stack.last()->children.last());
            }
        } else {
            if (!stack.isEmpty()) {
                Node *current = stack.last();
                if (!current->content.isEmpty()) {
                    current->content += '\n';
                }
                current->content += line;
            }
        }
    }
    return roots;
}

void LicenseViewer::addNode(const Node &node, QVBoxLayout *layout, int indent) {
    QWidget *header = new QWidget(this);
    QHBoxLayout *hbox = new QHBoxLayout(header);
    hbox->setContentsMargins(indent, 0, 0, 0);
    QLabel *label = new QLabel(node.title, header);
    QPushButton *button = new QPushButton("Show license", header);
    hbox->addWidget(label);
    hbox->addStretch();
    hbox->addWidget(button);

    QWidget *container = new QWidget(this);
    QVBoxLayout *containerLayout = new QVBoxLayout(container);
    containerLayout->setContentsMargins(indent + 20, 0, 0, 0);
    QTextEdit *text = new QTextEdit(node.content, container);
    text->setReadOnly(true);
    containerLayout->addWidget(text);

    QVBoxLayout *childLayout = new QVBoxLayout();
    containerLayout->addLayout(childLayout);
    container->setVisible(false);

    QObject::connect(button, &QPushButton::clicked, this, [container, button]() {
        bool vis = !container->isVisible();
        container->setVisible(vis);
        button->setText(vis ? "Hide license" : "Show license");
    });

    layout->addWidget(header);
    layout->addWidget(container);

    for (const auto &child : node.children) {
        addNode(child, childLayout, indent + 20);
    }
}

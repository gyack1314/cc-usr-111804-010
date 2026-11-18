# 灵巧手与关节交付资料的整机接口追溯

现有项目保存零部件接口与报告的冻结来源响应。transport 核对请求和原文字节，domain 提取来源声明的资料身份，ledger 原子保存版本，primary_records 与 supporting_records 分别展示两类已收业务原件，view 同时展示来源资料及待核状态。collection 将来源目录、待收范围与接收进度持久保存，archive 保留已发布视图所引用的资料状态；双来源初版资料已可按当前字段核对并判断发布；后续更正、撤回与范围变化尚待接续。合成样例不访问外部站点。来源字段见 docs/source-contract.md。

在项目根目录运行：

    python -m unittest discover -s tests -v
    python -m compileall -q capture_service tests
    python -m capture_service.cli inspect data/normal.json

容器运行：docker build -t robot-collection-010 .；docker run --rm robot-collection-010。

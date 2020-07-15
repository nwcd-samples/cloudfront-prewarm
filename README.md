# CloudFront 预热脚本

[CloudFront](https://aws.amazon.com/cn/cloudfront/?nc2=h_ql_prod_nt_cf) 为 AWS 的 CDN 服务。此脚本用于做 CloudFront 的预热。

CDN 已经为一项成熟且广泛应用的技术，其原理为 CDN POP 节点会缓存用户的请求，当下次附近的终端用户访问时，通过 PoP 点中的缓存直接返回内容，从而提高网站响应速度。
但当文件第一次被请求时，PoP 点是肯定没有缓存这个文件的，仍然需要到源站去请求。因此，首批请求此文件的用户可能会有比较慢的体验，不排除他们选择因此离开页面的可能性。对于一些视频网站来讲，这种痛点往往会更强烈。

此文提出针对解决这个问题的办法，即通过脚本把文件提前缓存到各个PoP点上。它的原理为向您需要的每个Pop点发起请求，请求成功后，此文件就缓存到您选择的这些 Pop 点上了。
对于一些流媒体的视频网站，文件量非常大，通常不需要预热所有的文件，只需要预热新影片片头的一些分片文件即可。

## 免责声明

建议测试过程中使用此方案，生产环境使用请自行考虑评估。

当您对方案需要进一步的沟通和反馈后，可以联系 nwcd_labs@nwcdcloud.cn 获得更进一步的支持。

欢迎联系参与方案共建和提交方案需求, 也欢迎在 github 项目 issue 中留言反馈 bugs。

## 使用方法

**1. 根据需求选择 PoP点**           
根据自己的需求，选择 PoP 点。CloudFront 在中国有4个节点（北京，宁夏中卫，深圳，上海），但在海外有 200+ 个节点，当我们做预热时，其实不需要将每个节点都预热到，只需要预热我们需要针对的终端用户所在位置即可。
比如如果您的 target user 为东南亚，只需要预热东南亚部分；同理，如果 target 在美国，只需要预热美国节点。
AWS 官方虽然没有对应的页面列出所有的 PoP 点的 code，但从一些第三方网站如[此网站](https://www.feitsui.com/zh-hans/article/3) 可以找到。
选择对应的 PoP code 并且生成 csv 文件。
> 注：中国区 Cloudfront 请用中国区的 POP Code，海外区 Cloudfront 请用海外的 PoP Code 

**2. 定义所需要预热的路径**     
   在 file.txt 中列出文件路径，或者是完整的访问连接。如：
   ```
   /btt1/2020/03/20200303/QoQQjVr1/2000kb/hls/XoLJyjuz.ts
   /btt1/2020/03/20200303/QoQQjVr1/2000kb/hls/1P5WgkfH.ts
   ```

或者是
   ```
   https://example.com/btt1/2020/03/20200303/QoQQjVr1/2000kb/hls/XoLJyjuz.ts
   https://example.com/btt1/2020/03/20200303/QoQQjVr1/2000kb/hls/1P5WgkfH.ts
   ```

**3. 参数定义**     
修改以下参数为您自己的参数。
```
domain = "example.com"  # 您的实际的自定义域名
cdn_name = 'd1s4q8j0xxxxx.cloudfront.net'
```

**4.运行脚本**    
通过 ```python3 __prewarm_update.py``` 运行此脚本。

## 自定义

如果存在您的 list 文件不同于样例中所示的格式等特殊情况，可以根据此脚本加以自定制。

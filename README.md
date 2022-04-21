<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<div align="center">

  <h1 align="center">UESTC_Login</h1>
  
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]

  <p align="center">
    电子科技大学统一身份认证自动化模拟登陆，可适用于网上服务大厅、教务系统、精准思政平台等众需要靠统一身份认证进行验证的网站或平台。
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## 效果演示

[![Product Name Screen Shot][product-screenshot]](https://example.com)

电子科技大学诸多校内网站都采用统一身份认证页面来进行验证，这意味着只需要一个登陆模板，就可以自动登陆大部分相关网站，自动获取其登录cookie并以此实现更多功能。

例如:
* 通过自动登录实现免抓包来进行的每日健康报送 [示例](https://github.com/Foreverddb/uestc_login/blob/master/%E8%87%AA%E5%8A%A8%E7%99%BB%E5%BD%95%E7%BD%91%E4%B8%8A%E6%9C%8D%E5%8A%A1%E5%A4%A7%E5%8E%85%E7%A4%BA%E4%BE%8B.py)
* 通过自动登录实现免跳转获取的本学期考试安排
* 通过自动登录实现免抓包进行的一卡通记录信息查询
* ......

Fork 此仓库或下载代码压缩包以立即开始使用， [点此查看使用指南](#开始使用)。

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## 开始使用

此项目使用非常简单，直接作为外部模块引入使用。

需要安装对应的浏览器驱动，目前貌似只有 FireFox 能正常运行，其他浏览器都加载不出页面来，还在适配中。

Firefox 对应驱动下载： [geckodriver](https://github.com/mozilla/geckodriver/releases)

### 作为模块引入


```python
import uestc_login
```
使用模块的方法：

`login() 方法` 返回一个 WebDriver 对象，可以通过 `driver.get_cookies()` 等方法获取登陆后页面的cookie等数据
- username： 学号
- password： 密码
- url： 需要登陆的网址，一般需要通过学校各种网站获取，例如网上服务大厅的认证网址为https://idas.uestc.edu.cn/authserver/login?service=https%3A%2F%2Feportal.uestc.edu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Feportal.uestc.edu.cn%2Fnew%2Findex.html%3Fbrowser%3Dno
- browser: 使用的浏览器，需要安装对应的浏览器驱动，可选（默认为 Firefox）
- hide： 是否以无UI界面形式运行，可选（默认为 False）

```python
import uestc_login
uestc_login.login(username='2021XXXXXXXXX', 
                  password='test', 
                  url='https://idas.uestc.edu.cn/authserver/login',
                  browser=uestc_login.FIREFOX,
                  hide=False) 
```


### 实现思路

使用 python + selenium 进行自动化登录，使用 opencv-python 来识别验证拼图位置并自动滑动滑块进行验证，同时也使用了 numpy 来进行一些多维数组的计算与处理。

* [OpenCV](https://opencv.org/)
* [Selenium](https://www.selenium.dev/)
* [Python](https://www.python.org/)
* [Numpy](https://numpy.org/)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[forks-shield]: https://img.shields.io/github/forks/Foreverddb/uestc_login.svg?style=for-the-badge
[forks-url]: https://github.com/Foreverddb/uestc_login/network/members
[stars-shield]: https://img.shields.io/github/stars/Foreverddb/uestc_login.svg?style=for-the-badge
[stars-url]: https://github.com/Foreverddb/uestc_login/stargazers
[issues-shield]: https://img.shields.io/github/issues/Foreverddb/uestc_login.svg?style=for-the-badge
[issues-url]: https://github.com/Foreverddb/uestc_login/issues
[license-shield]: https://img.shields.io/github/license/Foreverddb/uestc_login.svg?style=for-the-badge
[license-url]: https://github.com/Foreverddb/uestc_login/blob/master/LICENSE.txt
[product-screenshot]: images/demo.gif

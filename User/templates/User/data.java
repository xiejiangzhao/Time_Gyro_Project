PrintWriter out=response.getWriter();       //向客户端发送字符数据
 response.setContentType("text/text");          //设置请求以及响应的内容类型以及编码方式
response.setCharacterEncoding("UTF-8");
4         JSONArray  json = JSONArray.fromObject(newsList);   //将newsList对象转换为json对象
5         String str = json.toString();                //将json对象转换为字符串
6         out.write(str);
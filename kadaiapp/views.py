from django.shortcuts import render

from django.views.generic import TemplateView, ListView

from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import KadaiPostForm

from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

from .models import KadaiPost

from django.views.generic import DetailView

from django.views.generic import DeleteView

from django.views.generic import FormView

from .forms import ContactForm

from django.contrib import messages

from django.core.mail import EmailMessage


def Post(request):
    return render(request, 'Post.html')

def index_view(request):
    return render(request, 'index.html')

# class IndexView(ListView):
#     template_name = 'index.html'
    

class ContactView(FormView):
    '''問い合わせページを表示するビュー
    
    フォームで入力されたデータを取得し、メールの作成と送信を行う
    '''
    #contact.htmlをレンタリングする
    template_name = 'contact.html'
    #HTMLとDjangoを結ぶためのクラス
    form_class = ContactForm
    #送信完了後にリダイレクトするページ
    success_url = reverse_lazy('kadaiapp:contact')
    def form_valid(self, form):
        #フォームに入力されたデータをフィールド名を指定して取得
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        #メールのタイトルの書式を設定
        subject = 'お問い合わせ: {}'.format(title)
        #フォームの入力データの書式を設定
        message = \
            '送信者名: {0}\nメールアドレス: {1}\n タイトル:{2}\n メッセージ:\n{3}'\
                .format(name, email, title, message)
                #メールのお送信元のアドレス
        from_email = 'ooi2472021@stu.o-hara.ac.jp'
        #送信先のアドレス
        to_list = ['ooi2472021@stu.o-hara.ac.jp']
        #EmailMessageオブジェクトを作成
        message = EmailMessage(subject=subject,
                            body=message,
                            from_email=from_email,
                            to=to_list,
                            )
        #メールサーバーからメールを送信
        message.send()
        #送信完了後に表示するメッセージ
        messages.success(
            self.request, 'お問い合わせは正常に送信されました。')
        return super().form_valid(form)


class PhotoTitleView(TemplateView):
    template_name = 'photo_title.html'

class SaveView(ListView):
    template_name = 'save.html'
    
class IndexView(ListView):
    '''トップメニュー
    '''
    # index.htmlをレンダリングする
    template_name = 'index.html'
    #モデルBlogPostのオブジェクトにorder_by()を適用して
    #投稿日時の降順で並び替える
    queryset = KadaiPost.objects.order_by('-posted_at')
    # 1ページに表示するレコードの件数
    paginate_by = 9
#デコレーターにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
#ログイン状態でなければsettings.pyのLOGIN_URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    '''写真投稿ページのビュー

        PhotoPostFormで定義されているモデルとフィールドと連携して
        投稿データをデータベースに登録する

        Attributes:
        form_class: モデルとフィールドが登録されたフォームクラス
        template_name: レンダリングするテンプレート
        success_url: データベースへの登録完了後のリダイレクト先
    '''
    #forms.pyのPhotoPostFormをフォームクラスとして登録
    form_class = KadaiPostForm
    #レンダリングするテンプレート
    template_name = "post.html"
    #フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('kadaiapp:post_done')

    def form_valid(self, form):
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)

class PhotoSuccessView(TemplateView):
    '''投稿完了ページのビュー

    Attributes:
    template_name: レンダリングするテンプレート
    '''
    # index.htmlをレンダリングする
    template_name = 'post_success.html'

class CategoryView(ListView):
    '''カテゴリページのビュー

    Attributes:
    template_name: レンダリングするテンプレート
    paginate_by: 1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name = 'index.html'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = KadaiPost.objects.filter(
        category=category_id).order_by('-posted_at')
        return categories

class UserView(ListView):
    template_name = 'index.html'
    
    paginate_by = 9
    
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = KadaiPost.objects.filter(
            user=user_id).order_by('-posted_at')
        return user_list

class DetailView(DetailView):
    template_name = 'detail.html'
    
    model = KadaiPost
    

class MypageView(ListView):

    template_name='mypage.html'
    paginate_by= 9

    def get_queryset(self):

        queryset = KadaiPost.objects.filter(
        user=self.request.user).order_by('-posted_at')
        return queryset

class PhotoDeleteView(DeleteView):
    model = KadaiPost
    template_name= 'delete.html'
    success_url = reverse_lazy('kadaiapp:mypage')

    def delete(self, request,  *args, **kwargs):
        return super().delete(request, *args, **kwargs)


